import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_full_pipeline():
    print("Testing /api/health...")
    with client:
        # 1. Health
        res = client.get("/api/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        data = res.json()
        print("Health response:", data)
        assert data["status"] == "healthy"
        assert data["model_loaded"] is True
        assert len(data["classes"]) == 6

        # 2. Clear history before test
        client.delete("/api/history")

        # 3. Test Predictions with distinct emotions
        test_cases = [
            ("I am absolutely thrilled and ecstatic about winning first place!", "joy"),
            ("I feel completely devastated, empty, and heart-broken.", "sadness"),
            ("I am furious, livid, and totally outraged by their betrayal!", "anger"),
            ("I feel so tender and deeply in love with you forever.", "love"),
            ("I am terrified, panicked, and shaking in pure fear.", "fear"),
            ("I was completely shocked and astonished by the surprise party!", "surprise")
        ]

        print("\nTesting /api/predict with 6 emotional inputs...")
        for sentence, expected_emo in test_cases:
            res = client.post("/api/predict", json={"text": sentence})
            assert res.status_code == 200, f"Predict failed for '{sentence}': {res.text}"
            pred = res.json()
            prob_sum = sum(pred["probabilities"].values())
            print(f"Text: '{sentence[:40]}...' -> Predicted: {pred['predicted_emotion']} (Expected: {expected_emo}, Conf: {pred['confidence']:.2%}, Sum: {prob_sum:.4f})")
            assert pred["predicted_emotion"] == expected_emo, f"Expected {expected_emo}, got {pred['predicted_emotion']}"
            assert abs(prob_sum - 1.0) < 0.01, f"Probabilities do not sum to 1.0: {prob_sum}"
            assert "joy" in pred["probabilities"]
            assert "sadness" in pred["probabilities"]
            assert "anger" in pred["probabilities"]
            assert "love" in pred["probabilities"]
            assert "fear" in pred["probabilities"]
            assert "surprise" in pred["probabilities"]

        # 4. Test Empty and Invalid Inputs
        print("\nTesting validation on empty and whitespace inputs...")
        res_empty = client.post("/api/predict", json={"text": ""})
        assert res_empty.status_code == 422, f"Expected 422, got {res_empty.status_code}"

        res_space = client.post("/api/predict", json={"text": "     "})
        assert res_space.status_code == 422, f"Expected 422, got {res_space.status_code}"

        res_missing = client.post("/api/predict", json={})
        assert res_missing.status_code == 422, f"Expected 422, got {res_missing.status_code}"

        # 5. Test History Retrieval
        print("\nTesting /api/history...")
        res_hist = client.get("/api/history")
        assert res_hist.status_code == 200
        history = res_hist.json()
        print(f"Retrieved {len(history)} history records. Most recent: {history[0]['predicted_emotion']} -> '{history[0]['text'][:30]}...'")
        assert len(history) == 6

        # 6. Test Stats
        print("\nTesting /api/stats...")
        res_stats = client.get("/api/stats")
        assert res_stats.status_code == 200
        stats = res_stats.json()
        print("Stats:", stats)
        assert stats["total_records"] == 6

        # 7. Test History Deletion
        print("\nTesting DELETE /api/history...")
        res_del = client.delete("/api/history")
        assert res_del.status_code == 200
        del_data = res_del.json()
        assert del_data["deleted_count"] == 6

        res_hist_after = client.get("/api/history")
        assert len(res_hist_after.json()) == 0
        print("History cleared successfully!")

    print("\nALL BACKEND API TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    test_full_pipeline()

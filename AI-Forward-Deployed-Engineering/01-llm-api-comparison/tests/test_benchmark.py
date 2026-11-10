
import json

import benchmark


def test_load_prompts():
    prompts = benchmark.load_prompts()

    assert len(prompts) == 10

    for item in prompts:
        assert "id" in item
        assert "category" in item
        assert "prompt" in item
        assert item["prompt"].strip()


def test_unique_prompt_ids():
    prompts = benchmark.load_prompts()

    ids = [item["id"] for item in prompts]

    assert len(ids) == len(set(ids))


def test_save_results(tmp_path, monkeypatch):
    output_file = tmp_path / "results.json"

    monkeypatch.setattr(
        benchmark,
        "RESULTS_FILE",
        output_file
    )

    sample_results = [
        {
            "prompt_id": 1,
            "provider": "OpenAI",
            "status": "success",
            "response": "Example response"
        }
    ]

    benchmark.save_results(sample_results)

    assert output_file.exists()

    with open(output_file, encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == sample_results


def test_benchmark_dry_run(capsys):
    benchmark.run_benchmark(dry_run=True)

    output = capsys.readouterr().out

    assert "Loaded 10 benchmark prompts" in output
    assert "No API requests were made" in output

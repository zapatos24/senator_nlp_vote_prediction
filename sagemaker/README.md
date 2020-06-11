# Sagemaker model container

## Preparing model artifacts

Make sure that the latest model artifacts are in the following bucket:
https://s3.console.aws.amazon.com/s3/buckets/senator-nlp-vote-prediction/model_artifacts/?region=us-east-1&tab=overview

To quickly update these with local copies, place the following files in `model_artifacts` and run `make sync_models_to_s3`:

```
final_xgb_features.sav
final_xgb_model.sav
final_xgb_scaler.sav
```

## Local Docker development

From this directory, run `make build`

Then, run `make local_server` to run the docker container at http://localhost:8080.

Navigate to /ping to perform a health check, or post data to /invocations.


## Testing

For local testing, make sure the test file has `TEST_SERVER` set to `False` and run `python test/test.py`.

After deployment, to test the Sagemaker service run the same command with `TEST_SERVER` set to `True`.

## Deployment


Finally, from this directory, run `make build_and_push`

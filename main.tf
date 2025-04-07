data "aws_iam_policy_document" "assume_role"{
  statement {
    effect = "Allow"
    
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_lambda_layer_version" "dependencies_layer" {
  
  layer_name          = "dependencies-layer"
  compatible_runtimes = ["python3.13"]

  filename = "python.zip"
}

data "aws_iam_role" "telegram_user" {
  name = "Telegram_user"
}

resource "aws_lambda_function" "telegram_bot_lambda" {
  filename = "main.zip"
  function_name = "lambda_handler"
  role = data.aws_iam_role.telegram_user.arn

  source_code_hash = filebase64sha256("main.zip")

  runtime = "python3.13"

  environment {
    variables = {
      TELEGRAM_API_KEY = var.telegram_api
    }
  }

  layers = [
    aws_lambda_layer_version.dependencies_layer.arn
  ]
}
import boto3
import json

def lambda_handler(event, context):
    # Detalhes do evento S3
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    print(f"Arquivo carregado no bucket {bucket_name}: {object_key}")
    
    # Publicar mensagem no SNS
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:352245087617:s3-events-topic'  # Substitua pelo ARN do tópico SNS
    
    message = {
        "bucket": bucket_name,
        "object_key": object_key
    }
    
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message),
            Subject="Novo arquivo carregado no S3"
        )
        print(f"Mensagem publicada no SNS: {response['MessageId']}")
    except Exception as e:
        print(f"Erro ao publicar no SNS: {e}")
        raise
    
    return {
        'statusCode': 200,
        'body': f"Processado o arquivo {object_key} e notificação enviada"
    }

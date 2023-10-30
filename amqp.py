import pika, sys, os, logging, ssl
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get('ABLY_HOST')
username = os.environ.get('ABLY_USERNAME')
password = os.environ.get('ABLY_PASSWORD')
queue = os.environ.get('ABLY_QUEUE')


def main():


    context = ssl.create_default_context()

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,port=5671,virtual_host="shared",credentials=pika.PlainCredentials(username,password),
        ssl_options=pika.SSLOptions(context)))
    channel = connection.channel()



    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

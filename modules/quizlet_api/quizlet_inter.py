import os
import http.client as client

from quizlet import QuizletClient

CLIENT_ID = os.environ.get("CLIENT_ID")

def main():
    client = QuizletClient(client_id=CLIENT_ID, login="me")
    print(client.api.get("authorize", scope='write_set',
                                         client_id=CLIENT_ID,
                                         response_type='code',
                                         state='123'))
    print(client.sets.create(title="probe",
                             terms=["a",'b'],
                             lang_terms="en",
                             definitions=['c','d'],
                             lang_definitions='en'))


if __name__ == "__main__":
    main()
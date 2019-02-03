'''
actors add entries to msgboard to:
1. submit training votes (training)
2. commit suicide (training)
3. invalidate or validate others work proposals (work)
4. propose a work path (work)

actors always listens to it for:
1. training state change (training)
2. issuance of a state to goal (work)
3. others proposals for analysis (work)

actors listen directly to master for:
1. master to change their mode

So the ator has 3 threads that all run concurrently.
    1.  listens to master
    2.  listens to the messageboard
    3.  performs serial computation at the behest of the others
        (mostly finds paths, analyses paths, or produces votes)
'''

'''
I've been thinking about actor collaboration. in the naive version we can
create a new memory sturcture that is a distilation of the relationships within
each actor's memory: this/these state, at this value, given this action always
produces this/these states at the most granular level possible. that way each
actor has a predition for each way a state can change and can veto correctly.
but the correct way isn't to veto, it's just to fill in the missing elements of
state of a proposed action.
'''

import sys
from threading import Thread


def start_actor(
        input: dict,
        action: dict,
        state: dict,
        attention: list,
        actions: 'list(dict)'
    ) -> bool:
    actor = ActorNode(state, attention, actions, input, action)
    actor.listen_to('master')
    actor.listen_to('msgboard')
    return True

class ActorNode():
    ''' unit of reactive memory/computation '''

    def __init__(self,
        state: dict,
        attention: list,
        actions: 'list(dict)',
        input: dict = None,
        action: dict = None,
        verbose: bool = False,
        accepts_user_input: bool = False,
    ):
        ''' actor nodes contain little memory '''
        self.verbose = verbose
        self.exit = False
        if accepts_user_input:
            self.listen_to_user()




    def quit(self):
        self.exit = True
        exit()

    def listen_to(self, who: str):
        ''' concurrent listening '''
        def wire():
            print(f'listening to user input forever') if self.verbose else None
            commands = {
                'exit':self.quit, 'help':self.help_me,
                'start':self.help_me, 'explore':self.help_me, 'stop':self.help_me,
                'sleep':self.help_me, 'do':self.help_me,
            }

            while True:
                command = input('maestro> ')
                if command in commands.keys():
                    print(commands[command]())
                else:
                    print('invalid command. \n',self.help_me())

        threads = []
        threads.append(Thread(target=wire))

        try:
            threads[-1].start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

        print('listening to user input now') if self.verbose else None
        import time

        while True:
            time.sleep(10)
            if self.exit:
                sys.exit()
            print('sleeping')

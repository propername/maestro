'''
ConductorNode:
    interacts with the environment,
    creates MusicianNodes,
    and directs their behavior.
'''
import os
import sys
import time
import copy
import random
import threading

from maestro.core import musician
# only needed for typing annotation:
from maestro.simulations import env


class ConductorNode():
    ''' ConductorNode Object: there can be only one '''

    def __init__(
        self,
        environment: env.Environment,
        verbose: bool = False
    ):
        self.env = environment
        self.verbose = verbose
        self.exit = False
        self.state_keys = self.env.get_state_indexes()
        self.actions = self.env.get_actions()

        self.state = self.env.see()
        self.action = {}

        self.registry: 'dict(set(attention): bool)' = {}
        self.musicians: 'dict(set(attention): musician)' = {}

        self.goal = None

        # used in show
        self.last_print = ''

        # used to efficiently create musicians... not necessary any more...
        self.new = True
        self.voters = self.registry.keys()
        self.display_welcome()
        self.listen_to()

    def display_welcome(self):
        print('Welcome to Maestro AI, the naive sensorimotor inference engine!')
        print('\nMaestro is are running in Conductor mode.\n')
        print(
            'env', self.env.name,
            'allows for', len(self.env.get_actions()), 'actions',
            'and has', len(self.state_keys), 'state indicies.\n')
        print('maximum number of nodes:', 2 ** (len(self.state_keys)) - 2)

    def broadcast_message(self, msg: dict):
        if not self.new:
            for name, active in self.registry.items():
                if active:
                    self.musicians[name].add_message(msg)
        return msg

    def hear(self):
        if not self.new:
            for name, active in self.registry.items():
                if active:
                    self.musicians[name].process_last_message()

    def nap(self):
        for name, active in self.registry.items():
            if active:
                self.musicians[name].rest()

    # listen #################################################################

    def listen_to(self):
        ''' concurrent listening '''

        def user():
            ''' listens to user, upon command will modify configuration '''
            if self.verbose:
                print('\nconductor listening to user input forever')
            while True:
                if self.exit:
                    if self.verbose:
                        print('\nconductor shutting down user thread')
                    sys.exit()
                try:
                    self.handle_command(command=input('\nmaestro> '))
                except Exception:
                    self.quit()

        threads = []
        threads.append(threading.Thread(target=user))
        try:
            for thread in threads:
                thread.start()
            self.main_loop()
        except (KeyboardInterrupt, SystemExit):
            self.exit = True
            self.quit(1)

    def main_loop(self):
        while True:
            if self.exit:
                if self.verbose:
                    print('\nshutting down main_loop thread')
                self.quit()
            if self.goal == 'tune':
                msg = self.tune()
                self.hear()
                if self.verbose:
                    self.show(msg)
            elif self.goal == 'play':
                self.play()
            elif self.goal is None:
                self.sleep()

    def handle_command(self, command: str):
        ''' message from user, what should we do? '''
        commands = {
            'exit': self.quit,
            'help': self.help_me,
            'info': self.get_info,
            'tune': self.set_tune,
            'stop': self.set_stop,
            'sleep': self.nap,
            'dream': self.examine_sleep,
            'play': self.set_goal,
            'goal': self.set_goal,
            'do': self.perform_action,
            'send': self.send_message,
            'debug': self.debug,
            'clear': self.clear_screen,
            'pickle': self.export_pickle,
        }
        try:
            self.last_print = ''
            if command in commands.keys() and ' ' not in command:
                print('\n', commands[command]())
            elif command.split()[0] in [
                com.split()[0] for com in commands.keys()
            ]:
                print('\n', commands[command.split()[0]](*command.split()[1:]))
            else:
                print(f'\ninvalid command: {command}\n', self.help_me())
        except Exception as e:
            print(e)

    def handle_msg(self, msg):
        ''' message from musicians - what should we do with it? '''
        if self.goal == 'tune':
            # vote__msg = {'id':1, 'from':[1,2,3], 'vote':{0:'up'}}
            # TODO: handle death
            # hanle a death
            # for now we decide who dies, subsets...

            # TODO:
            # count the votes or
            # for now we are not couting votes, just acting randomly
            pass
        else:  # playing mode
            # TODO:
            # check if this message signals we have reached consensus or
            # if its a new proposal add it to the list
            pass

    # commands ###############################################################

    def get_info(self):
        return f'''
    maestro system information:

    conductor:
        mode: {'sleep' if self.goal==None else (
            'tune' if self.goal == 'tune' else 'play')}
        verbosity: {self.verbose}
        exit status: {self.exit}
        uptime: coming soon
        registry: {[
            str(k) + ':' + str(len(k)) for k,v in self.registry.items() if v]}
        current state: {self.state}
        latest action: {self.action}

    musicians:
        busy musicians: {[f'{k}:{len(self.musicians[k].inbox)} '
            for k,v in self.registry.items()
            if v and len(self.musicians[k].inbox) > 0]}
        musicians memory: {[f'{k}:{len(self.musicians[k].structure)} '
            for k,v in self.registry.items()
            if v and len(self.musicians[k].structure) > 0]}

    environment:
        name: {self.env.name}
        env: {self.env}
        state indicies: {self.state_keys}
        available actions: {self.env.get_actions()}

    '''

    def export_pickle(self):
        try:
            os.mkdir('musicians_data')
            for k, v in self.registry.items():
                if v:
                    self.musicians[k].structure.to_pickle(
                        f'musicians_data/{k}.pkl')
        except Exception:
            print('unable to make directory')

    def examine_sleep(self):
        try:
            os.mkdir('musicians_data')
        except Exception:
            print('unable to make directory')
            for k, v in self.registry.items():
                if v:
                    self.musicians[k].basics.to_pickle(
                        f'musicians_data/dreams-{k}.pkl')

    @staticmethod
    def help_me():
        return '''
    infomational commands:
    help        - display this message
    info        - display maestro system information
    clear       - clears screen

    behavioral commands:
    tune        - tells musicians to explore and learn
    stop        - tells musicians to stop all activity
    sleep       - tells musicians to condense memory
    play <goal> - tells maestro to achieve a goal
    exit        - exits maestro

    debug commands:
    do <goal>   - tells musicians to do an action
    send <msg>  - tells maestro to send a message
    debug <code>- tells maestro to execute code
    pickle      - exports pickles of musicians minds
    '''

    def quit(self, err: int = 0):
        self.exit = True
        sys.exit()

    def set_tune(self):
        self.goal = 'tune'
        return self.goal

    def set_stop(self):
        if self.new:
            self.create_musicians()
            self.new = False
        self.goal = None
        return self.goal

    def set_goal(self, *goal):
        if self.goal == 'tune' or self.goal is None:
            self.goal == ''
        if len(goal) == len(self.state_keys):
            self.goal = {k: v for k, v in zip(self.state_keys, goal)}
        else:
            return (
                f'error:\nspecified goal {goal} is not of the same length '
                + f'({len(goal)}) as the state representation for this'
                + f'environment ({len(self.state_keys)}).\nplease specify a'
                + f'value for each index in order:\n{self.state_keys}')

    def send_message(self, *message):
        message = ' '.join(message)
        return self.broadcast_message({'user': message})

    def debug(self, *code):
        code = ' '.join(code)
        return exec(code)

    def clear_screen(self):
        return os.system('cls')

    def perform_action(self, *action):
        action = ' '.join(action)
        return self.act(action)

    # main ###################################################################

    def show(self, msg: dict = None):
        if msg is None:
            counter = 0
            for x in self.registry:
                if self.registry[x]:
                    counter += 1
            info = 'state: {s}  |  action: {a}  |  registry: {r}'.format(
                s=str(self.state)[:10], a=str(self.action)[:10], r=counter)
        else:
            info = ''
            for k, v in msg.items():
                info = f'{info}{k}:{str(v)[:10]},'
                if len(info) >= 70:
                    break
        if self.last_print == 'show':
            print(info, end="\r", flush=True)
        else:
            print('')
            print(info, end="\r", flush=True)
            self.last_print = 'show'

    def tune(self):
        msg = {'from': 'conductor'}
        msg['last state'] = copy.deepcopy(self.state)
        self.action = random.choice(self.actions)
        self.state = self.act(self.action[0])
        msg['state'] = self.state
        msg['action'] = self.action
        return self.broadcast_message(msg)

    def sleep(self):
        time.sleep(1)

    def play(self):
        time.sleep(1)

    # behaviors ##############################################################

    def act(self, action):
        return self.analyze_state(self.env.act(action))

    def analyze_state(self, state) -> 'state':
        def get_keys_that_changed(state):
            return tuple([
                k for (k, v), (_, vv) in
                zip(sorted(self.state.items()), sorted(state.items()))
                if vv != v])

        def manage_registry(changed_keys):
            '''
            avoid creating or disable and remove musicians assigned to a subset
            of state indicies that another musician already pays attention to
            (according to the most naive algorithm).
            '''
            if changed_keys not in self.registry.keys():
                save = True
                for keys in self.registry.keys():
                    if len(changed_keys) < len(keys):
                        if set(changed_keys).issubset(keys):
                            save = False
                    elif set(keys).issubset(changed_keys):
                        self.registry[keys] = False
                if save:
                    self.make_musician(state=state, attention=changed_keys,)

        changed_keys = get_keys_that_changed(state)
        manage_registry(changed_keys)
        return state

    def make_musician(self, state: dict, attention: list):
        '''
        make a new musician, initialize it with state, attention and actions
        '''
        self.registry[attention] = True
        self.voters = self.registry.keys()
        if not self.new:
            self.musicians[attention] = musician.MusicianNode(
                state=state,
                attention=attention,
                actions=self.actions,
                verbose=self.verbose,)

    def create_musicians(self):
        '''
        create musicians for the first time afer we've quickly explored the env
        '''
        for attention, status in self.registry.items():
            if status:
                self.musicians[attention] = musician.MusicianNode(
                    state=self.state,
                    attention=attention,
                    actions=self.actions,
                    verbose=self.verbose,)

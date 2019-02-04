from .common import *

class ShellInvocationWrapper(threading.Thread):
    def __init__(self,invoke_command,shutdown_command, cwd=None):
        super(ShellInvocationWrapper,self).__init__()
        self.master_fd, self.slave_fd = pty.openpty()

        self.invoke_command = invoke_command
        self.shutdown_command = shutdown_command

        # use os.setsid() make it run in a new process group,
        # or bash job control will not be enabled
        self.p = subprocess.Popen(
                  invoke_command,
                  preexec_fn=os.setsid,
                  shell=True,
                  stdin=self.slave_fd,
                  stdout=self.slave_fd,
                  stderr=self.slave_fd,
                  close_fds=True,
                  cwd=cwd,

                  # Aki: discovered that without this, sudo will complain about
                  # no tty. Without shell=True, can't resize the tty
                  executable='/bin/bash',

                  universal_newlines=True)

    def set_size(self, row, col, xpix=0, ypix=0):
        """
        set the shell window size
        FROM: https://gareth.bult.co.uk/2016/07/23/a-terminal-solution/
        """
        winsize = struct.pack("HHHH", row, col, xpix, ypix)
        fcntl.ioctl(self.slave_fd, termios.TIOCSWINSZ, winsize)
        pgrp = os.getpgid(self.p.pid)
        os.killpg(pgrp,signal.SIGWINCH)

    def run(self):
        """ Get data from the pipe as it shows up and send it
            on to via publish to listening clients
        """
        while self.p.poll() is None:
            r, w, e = select.select([self.master_fd], [], [])
            if self.master_fd not in r:
                continue
            o = os.read(self.master_fd, 10240)
            if not o:
                continue
            self.data_from_process(o)

    def data_from_process(self,data):
        """ Subclass this to pass the data along to whatever
            application needs output from this command
        """
        pass

    def data_to_process(self,data):
        os.write(shell.master_fd, data)

    def shutdown(self):
        """ Subclass to handle what should happen when this session
            should close.
        """
        if self.shutdown_command:
            self.p = subprocess.Popen(
                self.shutdown_command,
                preexec_fn=os.setsid,
                shell=True,
                stdin=self.slave_fd,
                stdout=self.slave_fd,
                stderr=self.slave_fd,
                close_fds=True,

                # Aki: discovered that without this, sudo will complain about
                # no tty. Without shell=True, can't resize the tty
                executable='/bin/bash',

                universal_newlines=True
            )
            self.p.wait()
        else:
            pgrp = os.getpgid(self.p.pid)
            os.killpg(pgrp,signal.SIGTERM)


class ShellCommand(ShellInvocationWrapper):
    def __init__( self, command, wamp, session_id, uri, *args, **kwargs ):
        """

        command = ShellCommand(
                        command='/path/to/command/to/execute',
                        wamp=wamp,
                        uri='pubsub.uri',
                    )

        Then the output will be on:

        pubsub.uri.stdout

        And the terminal will respond to activity on

        pubsub.uri.stdin

        """

        cwd = os.getcwd()

        super(ShellCommand,self).__init__(
                    command,
                    None,
                    cwd=cwd,
                    *args,
                    **kwargs
                    )
        self.session_id = session_id
        self.wamp = wamp
        self.uri = uri
        self.uri_stdout = uri + '.stdout.{}'.format(session_id)
        self.uri_stdin = uri + '.stdin.{}'.format(session_id)

        """
        self.wamp.subscribe(
            self.uri_stdin,
            self.data_to_process
        )
        """

    def data_to_process(self,event):
        """ Receives data associated with a port and sends it to the
            underlying shell
        """
        key = event.args[0]
        os.write(session.shell.master_fd, key.encode('utf-8'))


    def data_from_process(self,data):
        """ Subclass this to pass the data along to whatever
            application needs output from this command
        """
        self.wamp.publish(
            self.uri_stdout,
            args=[base64.b64encode(data).decode('utf-8')]
        )


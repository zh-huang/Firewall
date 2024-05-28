import subprocess, re

class AppManager:

    def getNetworkConnections(self):
        try:
            result = subprocess.run(['ss', '-tulnp'], capture_output=True, text=True)
            return result.stdout.splitlines()
        except Exception as e:
            return ["Error: " + str(e)]

    def parseConnectionLine(self, line):
        parts = re.split(r'\s+', line)
        if parts[0] in ('tcp', 'udp'):
            proto = parts[0]
            local_address = parts[3]
            foreign_address = parts[4]
            state = parts[1] if proto == 'tcp' else ''
            pid_info = ' '.join(parts[6:]) if len(parts) > 6 else ''
            user, program, pid, fd = self.parsePidInfo(pid_info)
            return [user, program, pid, fd, proto, local_address, foreign_address, state]
        return ['', '', '', '', '', '', '', '']

    def parsePidInfo(self, pid_info):
        user = program = pid = fd = ''
        pid_pattern = re.compile(r'users:\(\("([^"]+)",pid=(\d+),fd=(\d+)\)\)')
        user_pattern = re.compile(r'^(\S+)')

        user_match = user_pattern.search(pid_info)
        pid_match = pid_pattern.search(pid_info)

        if user_match:
            user = user_match.group(1)
        if pid_match:
            program = pid_match.group(1)
            pid = pid_match.group(2)
            fd = pid_match.group(3)

        return user, program, pid, fd
    
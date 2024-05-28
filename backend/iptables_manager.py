import subprocess

class IptablesManager:
    def get_iptables_rules(self):
        command = ["iptables", "-L", "-n"]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Error executing iptables: {result.stderr}")

        lines = result.stdout.splitlines()
        data = []
        current_chain = None

        for line in lines:
            if line.startswith("Chain"):
                parts = line.split()
                current_chain = parts[1]
            elif line and current_chain:
                parts = line.split()
                if len(parts) >= 7:
                    data.append([current_chain, parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]])
        return data

    def add_rule(self, rule):
        try:    # INPUT -p tcp --dport 80 -j ACCEPT
            subprocess.run(['sudo', 'iptables','-A'] + rule.split(), check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f'Failed to add rule: {e}')

    def delete_rule(self, chain, target, prot, source, destination, ext):
        delete_command = ['sudo', 'iptables', '-D', chain, '-j', target, '-p', prot]
        if source != '0.0.0.0/0':
            delete_command += ['-s', source]
        if destination != '0.0.0.0/0':
            delete_command += ['-d', destination]
        if 'dpt' in ext:
            delete_command += ['--dport', ext.split(':')[1]]
        # Other extensions can be added here
        try:
            subprocess.run(delete_command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f'Failed to delete rule: {e}')

    def save_rules(self):
        result = subprocess.run(['iptables-save'], stdout=subprocess.PIPE, text=True)
        with open('iptables_rules.txt', 'w') as file:
            file.write(result.stdout)

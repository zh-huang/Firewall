import subprocess

class IptablesManager:
    def list_rules(self):
        result = subprocess.run(['sudo', 'iptables', '-L'], capture_output=True, text=True)
        return result.stdout

    def add_rule(self, rule):
        subprocess.run(['sudo', 'iptables', '-A'] + rule.split())

    def delete_rule(self, rule):
        subprocess.run(['sudo', 'iptables', '-D'] + rule.split())

    def save_rules(self):
        subprocess.run(['sudo', 'iptables-save', '>', '/etc/iptables/rules.v4'])

from cron import Cron


class CLICronManager:

    def __init__(self):
        self.crons = dict()

    def process(self, cli_string):
        try:
            cron = Cron(cli_string)
        except Exception as e:
            return None, e
        parsed_cron = cron.parsed_cron_breakdown()
        self.crons[cli_string] = cron
        return parsed_cron, None


if __name__ == '__main__':
    driver = CLICronManager()
    while True:
        cli_input = input("Add a New Cron : N || Show All Cron: S || Help: Help \n")
        if cli_input == 'N':
            input_string = input("Input cron-command string: \n")
            flattened_cron, exc = driver.process(input_string)
            if flattened_cron:
                print(flattened_cron)
                continue
            print(exc)
        elif cli_input == 'S':
            print(driver.crons)
        else:
            help_string = """ 
            This is cron schedule parser which flattens the schedule to  
            {Minute[], Hour[], Day[], Month[], Weekday[], Command} Format
            - N : Input Sting <Cron Schedule: Command>
            - S : Show All cron schedule and their commands added
            """
            print(help_string)

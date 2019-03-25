class Leg:
    pass


class Back:
    pass


class Chair:
    def __init__(self, num_legs):
        self.legs = [Leg() for number in range(num_legs)]
        self.back = Back()

    def __repr__(self):
        return "It's a chair with: \n" \
               "{} legs and \n" \
               "{} back.".format(len(self.legs), 1)


print((Chair(num_legs=5)))

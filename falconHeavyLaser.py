from test_NeatoCommands import envia


def enable_laser(ser, b):
        """ Activates or deactivates the laser depending on whether the value of b is True or False. """
        # msg = ''

        if b:
            msg = envia(ser, 'SetLDSRotation On')
            print("Enable Laser\n")
        else:
            msg = envia(ser, 'SetLDSRotation Off')
            print("Disable Laser\n")

        if msg != '\032':
            print("[ROBOT LASER]", msg)


def get_laser(ser):
        """ Ask to the robot for the current values of the laser. """
        msg = envia(ser, 'GetLDSScan')
        # print(msg)
        ret = []
        for line in msg.split('\r\n')[2:362]:
            s = line.split(',')
            lr = [s[0], s[1], s[2], s[3]]
            ret.append(lr)
        return ret

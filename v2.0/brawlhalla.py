import sys
sys.path.append('util/')

import record_proxy
import logging_utils

def main():
    prox = record_proxy.TransparentProxy("192.168.88.13", 50000, False)  # Listen for a TCP connection on localhost port 50000(binded in /etc/hosts).
    logging_utils.logpr(prox)
    prox.run()

    
    
if __name__ == "__main__":
    print("\n")
    main()
    print("\n")
else:
    logging_utils.logpr(f"Only use \"{BASENAME}\" as a script!")
    sys.exit()

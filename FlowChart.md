# Syndra Flowchart

# Setup Command

 - Setup Command
    - Setup currency (server_id)
    - Setup Role Pay (user_id/role_id)

# Mail

Mail proccess (receiver):
1. Mail Init
    - Create Mail instance
    - Notify User
2. Mail Read
    * 2.1 - Mail Replied
        - Update Mail instance
        - Mail init (sender) | Mail read, replied :: 
    * 2.2 - Mail Delayed
        - Mail init (sender) | Mail read, replied DELAYED, amount of time ::, reason ::

Mail proccess (sender):
1. Mail Init
    - Create Mail instance
    - Notify User
2. Mail Read
    * 2.1 - Mail Accepted
        - Update Mail instance
        - Mail init (reciever) | Mail read, product ACCEPTED
    * 2.2 - Mail Declined
        - Update Mail Instance
        - Mail init (reciever) | Mail read, procduct DENIED, reason ::
    * 2.3 - Recevier Delayed
        - Update Mail Instance
        - Lock Delay (amount of time)
        - Unlock
        - Await interaction (sender)
        - reinit (reciever) `` loop

# Trade Command

 - Trade Command
    - Create Trade
        - Statis funds
    - 3 level verification
        - Return to sender Verification
        - Recevier Verification && [[FlowChart#Mail|Mail]] init (reciever)
        - Return to sender Verification && [[FlowChart#Mail|Mail]] init (sender)
    - Complete Trade
        - Shift Funds

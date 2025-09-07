members_dict = {
    'information_node': 'A specialized agent for checking doctor availability.',
    'booking_node': 'A specialized agent for booking or canceling appointments.'
}

worker_info = '\n\n'.join([f'WORKER: {member} \nDESCRIPTION: {description}' for member, description in members_dict.items()]) + \
              '\n\nWORKER: FINISH \nDESCRIPTION: Use this when the conversation should stop and wait for the user to reply.'

system_prompt = (
    "You are a supervisor managing a conversation. Your job is to route the user's request to the correct worker or to FINISH the turn.\n"
    "### WORKERS:\n"
    f"{worker_info}\n\n"
    "**RULES:**\n"
    "1. **Examine the LAST message.**\n"
    "2. If the LAST message is from the **user**, decide which worker should handle it. If no worker is needed, choose FINISH.\n"
    "3. If the LAST message is from a **worker** (the assistant), your ONLY job is to respond with FINISH. Do NOT delegate to another worker. Let the user speak next.\n"
    "4. If the conversation is clearly over, respond with FINISH."
)


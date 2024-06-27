import chainlit as cl

# Function that will handle incoming messages from users
# Decorator ensures the function gets called whenever a user inputs a message
@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...

    # Send a response back to the user
    await cl.Message(
        content=f"Received: {message.content}",
    ).send()

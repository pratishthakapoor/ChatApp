from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    CardFactory,
    UserState,
    MessageFactory,
)
from botbuilder.schema import (
    ChannelAccount,
    Attachment,
    Activity,
    ActivityTypes,
    HeroCard,
    AttachmentData,
    CardImage,
    CardAction,
    ActionTypes,
)

from data_models import WelcomeUserState


class WelcomeBot(ActivityHandler):
    member_name = ""
    
    def __init__(self, user_state: UserState):
        if user_state is None:
            raise TypeError(
                "[WelcomeUserBot]: Missing parameter. user_state is required but None was given")
        self.user_state = user_state

        self.user_state_accessor = self.user_state.create_property("WelcomeUserState")

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # save chnages to WelcomeUserState after each turn
        await self.user_state.save_changes(turn_context)
        
    async def on_message_activity(self, turn_context: TurnContext):
        # Get the state properties from the turn context
        welcome_user_state = await self.user_state_accessor.get(turn_context, WelcomeUserState)
        if not welcome_user_state.did_welcome_user:
            welcome_user_state.did_welcome_user = True
        else:
            text = turn_context.activity.text.lower()
            if text in ("hello", "hi"):
                await turn_context.send_activity(f"You said { text }")
            elif text in ("intro", "help"):
                await self.__send_intro_card(turn_context)
            else:
                await turn_context.send_activity("Please provide an input")

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
        ):
        """
        Greet when users are added to the conversation.
        Note that all channels do not send the conversation update activity.
        If you find that this bot works in the emulator, but does not in
        another channel the reason is most likely that the channel does not
        send this activity.
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                reply = MessageFactory.list([])
                member_name = member.name
                message = Activity(
                    type=ActivityTypes.message,
                    attachments=[self.__send_welcome_card(member_name)],
                )

                await turn_context.send_activity(message)

                #await self.__send_welcome_card(turn_context, member_name)
                

##                await turn_context.send_activity(
##                """It is a good pattern to use this event to send general greeting
##                    to user, explaining what your bot can do. In this example, the bot
##                    handles 'hello', 'hi', 'help' and 'intro'. Try it now, type 'hi'"""
##            )


    def __send_welcome_card(self, member_name) -> Attachment:
        ADAPTIVE_CARD_CONTENT = {
    "type": "AdaptiveCard",
    "version": "1.0",
    "body": [
        {
            "type": "ImageSet",
            "images": [
                {
                    "type": "Image",
                    "horizontalAlignment": "Center",
                    "url": "https://www.smallbizgenius.net/wp-content/uploads/2019/10/chatbot-4071274_1920_710x473.jpg",
                    "id": "Image1",
                    "spacing": "None",
                    "separator": True,
                    "size": "Large",
                    "height": "stretch"
                }
            ],
            "horizontalAlignment": "Left",
            "id": "",
            "spacing": "Padding",
            "imageSize": "Large"
        },
        {
            "type": "TextBlock",
            "text": "Welcome to WeChat! I am developed to provide you with latest news update",
            "horizontalAlignment": "Center",
            "wrap": True,
            "fontType": "Monospace",
            "color": "Dark",
            "size": "Large",
        }
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
}
        #print(type(CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT)))
        return CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT)

    async def __send_intro_card(self, turn_context: TurnContext):
        card = HeroCard(
            title="Welcome to Bot Framework!",
            text="Welcome to Welcome Users bot sample! This Introduction card "
            "is a great way to introduce your Bot to the user and suggest "
            "some things to get them started. We use this opportunity to "
            "recommend a few next steps for learning more creating and deploying bots.",
            images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                type=ActionTypes.open_url,
                title="Get an overview",
                text="Get an overview",
                display_text="Get an overview",
                value="https://docs.microsoft.com/en-us/azure/bot-service/?view=azure-bot-service-4.0",
                ),
                CardAction(
                    type=ActionTypes.open_url,
                    title="Ask a question",
                    text="Ask a question",
                    display_text="Ask a question",
                    value="https://stackoverflow.com/questions/tagged/botframework",
                ),
                CardAction(
                    type=ActionTypes.open_url,
                    title="Learn how to deploy",
                    text="Learn how to deploy",
                    display_text="Learn how to deploy",
                    value="https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-howto-deploy-azure?view=azure-bot-service-4.0",
                ),
            ],
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(card))
        )
    

                

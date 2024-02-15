extern crate dotenv;

use dotenv::dotenv;
use std::env;

use serenity::{
    async_trait,
    model::{channel::Message, gateway::Ready},
    prelude::*
};

// Command Handler


// Event Handler

struct Handler;

#[async_trait]
impl EventHandler for Handler {
    // on_message
    async fn message(&self, ctx: Context, msg: Message) {
        if msg.content == "!ping" {
            if let Err(why) = msg.channel_id.say(&ctx.http, "Pong!").await {
                println!("Error sending message: {:?}", why);
            }
        }
    }

    // on_ready
    async fn ready(&self, _: Context, ready: Ready) {
        println!("{} is connected!", ready.user.name);
    }
}


// Main Loop (async)
#[tokio::main]
async fn main() {
    // Get Discord Token
    dotenv().ok();
    
    // Get Token from .env
    let token = env::var("DISCORD_TOKEN")
        .expect("Expected a token in the environment");

    // Create Client
    let mut client = Client::builder(&token, GatewayIntents::all())
        .event_handler(Handler)
        .await
        .expect("Err creating client");

    // Start Client
    if let Err(why) = client.start().await {
        println!("Client error: {:?}", why);
    }
}

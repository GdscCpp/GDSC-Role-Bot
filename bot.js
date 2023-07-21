const { Client, GatewayIntentBits } = require("discord.js");
const secrets = require("./secrets");
const { exec } = require("child_process");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers,
  ],
});

client.on("ready", async () => {
  console.log(`Logged in as ${client.user.tag}!`);

  //setTimeout(async () => {
  let cmd = "python ./get_tags.py";

  exec(
    cmd,
    async (err, data, stderr) => {
      if (err || stderr) {
        console.log(err || stderr);
      }

      data = data.split("\n");
      tags = data.slice(0, -2)[0];
      tags = tags.replaceAll("'", '"');
      tags = JSON.parse(tags);

      //filter through results and assign roles
      console.log("Fetching users...");
      let guild = await client.guilds.fetch(secrets.TEST_SERVER_ID);

      console.log("Fetching role...");
      let role = guild.roles.cache.find(
        (role) => role.name === "General Member"
      );

      console.log("Fetching members...");

      guild.members.fetch().then((members) => {
        members.map((member) => {
          for (let i = 0; i < tags.length; i++) {
            if (
              tags[i][0] + "#0" == member.user.tag ||
              tags[i][0] == member.user.tag
            ) {
              member.roles.add(role);
              console.log("Role added for " + member.user.tag);
            }
          }
        });
      });

      console.log("Roles updated");
    }

    //}, 2000);
  );
});

client.login(secrets.TOKEN);

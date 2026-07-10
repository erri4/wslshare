const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client({
    authStrategy: new LocalAuth()
});

let allowOthers = false;

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('Bot is running! Default: Only responding to YOU.');
});

const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json()); // Allows parsing JSON payloads from your frontend

const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('message_create', async (msg) => {
    if (msg.body !== '1434' && (!msg.body || !msg.body.startsWith('!'))) return;

    const args = msg.body.slice(1).trim().split(/ +/);
    let command = args.shift().toLowerCase();
    if (msg.body === '1434') command = '1434';

    let chat;
    try {
        chat = await msg.getChat();
    } catch (err) {
        console.error('Failed to get chat:', err);
        return;
    }

    if (command === 'toggle') {
        if (!msg.fromMe) return;

        allowOthers = !allowOthers;

        const statusMessage = allowOthers
            ? "*Bot Access Opened:* Other users can now use commands!"
            : "*Bot Access Closed:* Only I can use commands now.";

        await msg.reply(statusMessage);
        return;
    }

    if (command === 'latex'){
        const encodedFormula = encodeURIComponent(formula);
        const apiUrl = `https://erri4.github.io/wslshare/katex/?latex=${encodedFormula}`;
        
        const media = await MessageMedia.fromUrl(apiUrl);

        await client.sendMessage(targetChatId, media, {
            caption: `Rendered LaTeX formula: ${formula}`
        });
    }

    if (!allowOthers && !msg.fromMe) {
        return;
    }


    if (command === '1434' && chat.isGroup) {
        try {
            const participants = chat.participants;
            const BATCH_SIZE = 250;

            if (participants.length <= BATCH_SIZE) {
                const mentions = participants.map(p => p.id._serialized);
                await chat.sendMessage('נפסלתי', { mentions });
            } else {
                for (let i = 0; i < participants.length; i += BATCH_SIZE) {
                    const batch = participants.slice(i, i + BATCH_SIZE);
                    const mentions = batch.map(p => p.id._serialized);
                    await chat.sendMessage('נפסלתי', { mentions });
                }
            }
        } catch (err) {
            console.error('!all failed:', err);
            await msg.reply('Failed to tag everyone (group might be too large or something went wrong).');
        }
        return;
    }

    if (command === 'steal') {
        if (!msg.hasQuotedMsg) {
            await msg.reply('Reply to a sticker with !steal to grab it.');
            return;
        }
        try {
            const quotedMsg = await msg.getQuotedMessage();
            if (quotedMsg.hasMedia && quotedMsg.type === 'sticker') {
                const media = await quotedMsg.downloadMedia();
                await chat.sendMessage(media, { caption: 'Sticker stolen!' });
            } else {
                await msg.reply('That quoted message isn\'t a sticker.');
            }
        } catch (err) {
            console.error('!steal failed:', err);
            await msg.reply('Something went wrong grabbing that sticker.');
        }
        return;
    }
});

client.initialize();
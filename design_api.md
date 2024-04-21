# Table of content

-   [Authentication](#authentication)
-   [Channels](#channels)
-   [Objects](#objects)

## Per modules

-   **Tokens**

    -   [Create new Bearer token](#create-new-bearer-token)
    -   [Refresh access token](#refresh-access-token)

-   **Auth**

    -   [Login](#login)
    -   [Register](#register)
    -   [Logout](#logout)
    -   [Switch OTP status](#switch-otp-status)
    -   [Post OTP status](#post-otp-status)
    -   [Get OTP status](#get-otp-status)
    -   [Get OTP code](#get-otp-code)
    -   [Check OTP code](#check-otp-code)
    -   [Get an OTP QR code](#get-otp-qr-code)

-   **Users**

    -   [Get information about yourself](#get-my-profile)
    -   [Update my profile](#update-my-profile)
    -   [Get my profile avatar](#get-my-profile-avatar)
    -   [Upload my profile avatar](#upload-my-profile-avatar)

-   **Channels**

    -   [Create a channel](#create-channel)
    -   [List channels are seen by user](#list-channels-by-user)
    -   [Get a channel are seen by user](#get-a-channel-by-user)
    -   [Update a channel by owner](#update-channel-by-owner)
    -   [Add new admin by owner](#add-new-admin-by-owner)
    -   [Remove admin by owner](#remove-admin-by-owner)
    -   [Join a channel](#join-a-channel)
    -   [Leave a channel](#leave-a-channel)
    -   [Ban a user in a channel by admin](#ban-a-user-in-channel-by-admin)
    -   [Unban a user in a channel by admin](#unban-a-user-in-channel-by-admin)
    -   [Mute user in a channel by admin](#mute-user-in-channel-by-admin)
    -   [Unmute user in a channel by admin](#unmute-user-in-channel-by-admin)
    -   [Invite user in a channel by admin](#invite-user-in-channel-by-admin)
    -   [Update the user's invitation status](#update-users-invitation-status)
    -   [Send a message in a channel](#send-message-in-channel)
    -   [Get a list of user messages in a channel](#get-list-users-messages-in-channel)
    -   [Update the content of a message](#update-the-content-of-a-message)
    -   [Get a list last 50 messages in a channel](#get-list-last-50-messages-in-channel)
    -   [Get list of friends of a user](#get-list-of-friends-of-a-user)

-   **Friendship**

    -   [Invite a user to be a friend](#invite-user-to-be-friend)
    -   [Update the status of user's invitation](#update-status-of-users-invitation)
    -   [Get a list of friend invitations sent by a user](#get-list-of-friend-invitations-sent-by-an-user)
    -   [Get a list of friend invitations received by a user](#get-list-of-friend-invitations-received-by-an-user)
    -   [Ban user from sending a friend invitation](#ban-user-from-sending-a-friend-invitation)
    -   [Unban user from sending a friend invitation](#unban-user-from-sending-a-friend-invitation)
    -   [Mute user from sending private messages](#mute-user-from-sending-private-messages)
    -   [Unmute user from sending private messages](#unmute-user-from-sending-private-messages)

-   **User Messages**

    -   [Send a message to a friend](#send-message-to-a-friend)
    -   [Get list of last 50 messages sent to a friend](#get-list-last-50-messages-sent-to-a-friend)
    -   [Update the content of a message](#update-the-content-of-a-message)

-   **Games**

# Authentication

For every route, except `/register`, `/login` and `/otp/status` you need to provide a Bearer token in the request headers.

```
authorization: Bearer <token>
```

## Create new Bearer token

Create new access token and refresh token for a user

```typescript
POST /api/v1/token
{
	username: string,
	password: string,
}
```

### Return

```typescript
{
	refresh: string,
	access: string
}
```

## Refresh access token

When the access token expires, you can use the refresh token to get a new access token.

```typescript
POST / api / v1 / token / refresh;
{
    refresh: string;
}
```

### Return

```typescript
{
    access: string;
}
```

## Login

```typescript
POST /api/v1/auth/login
{
	username: string,
	password: string,
	otp: string (optional)
}
```

Login with this username, password and an optional TOTP

### Return

```typescript
{
	message: string
	refresh: string,
	access: string
}
```

## Register

```typescript
POST /api/v1/auth/register
{
	username: string,
	password: string,
	email: string,
	first name: string,(optional)
	last name: string(optional)
}
```

### Return

```typescript
{
    message: string;
}
```

Register a user if it doesn't exist

## Logout

```typescript
POST /api/v1/auth/logout
authorization Bearer <token>
```

### Return

```typescript
{
    message: string;
}
```

## Switch OTP status

```typescript
POST /api/v1/auth/otp/switch
authorization Bearer <token>
```

### Return

```typescript
{
    otpStatus: boolean;
}
```

Switch OTP status: true -> false, false -> true

## Post OTP status

Anyone can get OTP status with a username and password

```typescript
POST /api/v1/auth/otp/status
{
	username: string,
	password: string
}
```

### Return

```typescript
{
    otpStatus: boolean;
}
```

## Get OTP status

Only authenticated user can get OTP status

```typescript
GET /api/v1/auth/otp/status
authorization Bearer <token>
```

### Return

```typescript
{
    otpStatus: boolean;
}
```

## Get OTP code

```typescript
GET /api/v1/auth/otp
authorization Bearer <token>
```

### Return

```typescript
{
    otp: string;
}
```

Get OTP of a user

## Check OTP code

```typescript
POST /api/v1/auth/otp/check
{
	otp: string
}
authorization Bearer <token>
```

### Return

```typescript
{
    message: string;
}
```

Check OTP of a user

## Get OTP QR code

```typescript
GET /api/v1/auth/otp/qr-code
authorization Bearer <token>
```

### Return

-   The OTP QR code ([QRCode](#qrcode)) type image/png

## Get my profile

```typescript
GET /api/v1/profile/me
authorization Bearer <token>
```

### Return

-   The user profile ([User](#user))

## Update my profile

```typescript
PUT /api/v1/profile/me
authorization Bearer <token>
{
	... new data ...
}
```

### Return

-   The updated user profile ([User](#user))

## Get my profile avatar

```
GET /api/v1/profile/me/avatar
authorization Bearer <token>
```

### Return

-   The user's profile avatar ([UserAvatar](#useravatar))

Retrieve the user's profile avatar from backend storage

## Upload my profile avatar

```typescript
POST /api/v1/profile/me/avatar
authorization Bearer <token>
avatar: File
```

### Return

```typescript
{
    message: string;
}
```

Upload a profile avatar, save it in the backend and update the user's avetarPath in the database

For frontend implementation, see: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#uploading_a_file

# Channels

Public channel: every user can see it and join it.
Private channel: only the members and invited users can see it. Only invited users can join it.

## Create channel

```typescript
POST /api/v1/channel/create
authorization Bearer <token>
{
	name: string,
	visibility: 'public' | 'private',//optional
	password: string, //optional
}
```

### Return

```typescript
{
    message: string;
}
```

Create a new channel for a user. The user will be the owner of the channel and be added to the list of admins and members

## List channels by user

```typescript
GET /api/v1/channel/list
authorization Bearer <token>
```

### Return

-   A list of channel objects ([Channel](#channel))

List every channel the user can see: public channels, channels in which the user is invited or is a member

## Get a channel by user

```
GET /api/v1/channel/<channel_id>
authorization Bearer <token>
```

### Return

-   The channel object ([Channel](#channel))

## Update channel by owner

Only the channel's owner can update the channel1

```typescript
PUT /api/v1/channel/<channel_id>
authorization Bearer <token>
{
	"name": string, // optionnal
	"visibility": 'public' | 'private', // optionnal
	"password": string // optionnal
}
```

### Return

-   The updated channel object ([Channel](#channel))

Update the name, visibility or password of a channel by an admin

## Add new admin by owner

Only the channel's owner can add a user as an admin and the user must be a member of the channel and isn't already an admin of the channel

```typescript
POST /api/v1/channel/<channel_id>/admin/add
authorization Bearer <token>
{
	"username": string
}
```

### Return

```typescript
{
    message: string;
}
```

## Remove admin by owner

Only the channel's owner can remove a user as an admin. The user must be an admin of the channel

```typescript
POST /api/v1/channel/<channel_id>/admin/remove
authorization Bearer <token>
{
	"username": string
}
```

### Return

```typescript
{
    message: string;
}
```

## Join a channel

Every one can join a public channel. Only invited users can join a private channel. If user is banned from the channel,
he can't join it. The user have to provide a password to join if the channel's password is set. The user will be added
to the list of members of the channel.

```typescript
POST /api/v1/channel/<channel_id>/join
authorization Bearer <token>
```

### Return

-   The joined channel object ([Channel](#channel))

## Leave a channel

Only members can leave a channel. If the user is a admin of this channel, he is removed from the list of admins and members.

```typescript
POST /api/v1/channel/<channel_id>/leave
authorization Bearer <token>
```

### Return

-   The leaved channel object ([Channel](#channel))

## Ban a user in channel by admin

You must be an admin to ban a user from a channel. If this user is actually a member of the channel, he will be removed
from the list of members. You can't ban an admin or owner of the channel. If until is not provided, until will be set to
the Max Date.

```typescript
POST /api/v1/channel/<channel_id>/member/ban
authorization Bearer <token>
{
	"username": string
	"until": string // ISO date format YYYY-MM-DD // optional
	"reason": string // optional
}
```

### Return

-   The channel banned user object ([ChannelBannedUser](#channelbanneduser))

## Unban a user in channel by admin

You must be an admin to unban a user from a channel. If the user isn't on the banned list, an error will be raised. The
until field will be update to the Min Date.

```typescript
POST /api/v1/channel/<channel_id>/member/unban
authorization Bearer <token>
{
	"username": string
}
```

### Return

-   The updated banned user object ([ChannelBannedUser](#channelbanneduser))

## Mute user in the channel by admin

You must be an admin to mute a user from a channel. The owner and admin can't be muted. If until is not provided, until
will be set to the Max Date.

```typescript
POST /api/v1/channel/<channel_id>/member/mute
authorization Bearer <token>
{
	"username": string
	"until": string // ISO date format YYYY-MM-DD // optional
	"reason": string // optional
}
```

### Return

-   The channel muted user object ([ChannelMutedUser](#channelmuteduser))

## Unmute user in channel by admin

You must be an admin to unmute a user from a channel. If the user isn't muted, error will be raised. The until field will
be update to the Min Date.

```typescript
POST /api/v1/channel/<channel_id>/member/unmute
authorization Bearer <token>
{
	"username": string
}
```

### Return

-   The updated channel muted user object ([ChannelMutedUser](#channelmuteduser))

## Invite user in channel by admin

Only channel's admin can invite users in the channel.

```typescript
POST /api/v1/channel/<channel_id>/member/invite
authorization Bearer <token>
{
	"username": string
}
```

### Return

-   The invited user object ([ChannelInvitedUser](#channelinviteduser))

## Update user's invitation status

Only channel's admin can update status of user's invitation.

```typescript
PUT /api/v1/channel/<channel_id>/member/invite
authorization Bearer <token>
{
	"username": string,
	"status": string // 'accepted' | 'pending' | 'rejected'
}
```

### Return

-   The updated invited user object ([ChannelInvitedUser](#channelinviteduser))

## Send message in channel

The sender and receiver must be members of the channel

```typescript
POST /api/v1/channel/<channel_id>/message
authorization Bearer <token>
{
	"content": string
}
```

### Return

-   A ChannelMessage object ([ChannelMessage](#channelmessage))

## Get list user's messages in channel

Display a list of messages in channel sent by the user

```typescript
GET /api/v1/channel/<channel_id>/message
authorization Bearer <token>
```

### Return

-   A list of ChannelMessage objects ([ChannelMessage](#channelmessage))

## Update the content of a message

Only the sender of the message can update the content of the message

```typescript
PUT /api/v1/channel/<channel_id>/message/<message_id>
authorization Bearer <token>
{
	"content": string
}
```

### Return

-   The updated ChannelMessage object ([ChannelMessage](#channelmessage))

## Get list last 50 messages in channel

```typescript
GET /api/v1/channel/<channel_id>/message/last
authorization Bearer <token>
```

### Return

-   A list of ChannelMessage objects ([ChannelMessage](#channelmessage))

## Invite user to be friend

If the user is already friend, error will be raised. If the user is banned from another user, error will be raised.
Otherwise a new friendship will be created.

```typescript
POST /api/v1/user/friendship/invite
authorization Bearer <token>
{
	"username": string
}
```

### Return

-   A Friendship object ([Friendship](#friendship))

## Update status of user's invitation

Only receiver of the invitation can update status of user's invitation.

```typescript
PUT /api/v1/user/friendship/<friendship_id>/status
authorization Bearer <token>
{
	"status": string // 'accepted' | 'pending' | 'rejected'
}
```

### Return

-   A updated Friendship object ([Friendship](#friendship))

## Get list of friend invitations sent by a user

```typescript
GET /api/v1/user/friendship/sent
authorization Bearer <token>
```

### Return

-   A list of Invitation objects ([Invitation](#invitation))

## Get list of friend invitations received by a user

```typescript
GET /api/v1/user/friendship/received
authorization Bearer <token>
```

### Return

-   A list of Invitation objects ([Invitation](#invitation))

## Get list of friends of a user

Return a list of Friendship objects ([Friendship](#friendship)) where the status field is 'accepted'.

```typescript
GET /api/v1/user/friendship
authorization Bearer <token>
```

### Return

-   A list of Friendship objects ([Friendship](#friendship))

## Ban user from sending a friend invitation

If the user is already banned, error will be raised. Otherwise a new bannedUser will be created or updated. If the until
field is not set, it will be set to the Max Date.

```typescript
POST /api/v1/user/friendship/ban
authorization Bearer <token>
{
	"username": string,
	"until": string, // YYYY-MM-DD // optional
	"reason": string // optional
}
```

### Return

-   A BannedUser object ([BannedUser](#banneduser))

## Unban user from sending a friend invitation

If the user is not banned, error will be raised. If the until field is not set, it will be set to the Min Date.

```typescript
POST /api/v1/user/friendship/unban
authorization Bearer <token>
{
	"username": string
}
```

### Return

-   An updated bannedUser object ([BannedUser](#banneduser))

## Mute user from sending private messages

```typescript
POST /api/v1/user/friendship/mute
authorization Bearer <token>
{
	"username": string,
	"until": string, // YYYY-MM-DD // optional
	"reason": string // optional
}
```

### Return

-   A MutedUser object ([MutedUser](#muteduser))

## Unmute user from sending private messages

```typescript
POST /api/v1/user/friendship/unmute
authorization Bearer <token>
{
	"username": string
}
```

### Return

-   A updated MutedUser object ([MutedUser](#muteduser))

## Send a message to a friend

Only friend can send a message to a friend

```typescript
POST /api/v1/user/friend/message
authorization Bearer <token>
{
	"username": string,
	"content": string
}
```

### Return

-   A UserMessage object ([UserMessage](#usermessage))

## Get list of last 50 messages sent to a friend

```typescript
GET /api/v1/user/friend/<friend_id>/message/last
authorization Bearer <token>
```

### Return

-   A list of UserMessage objects ([UserMessage](#usermessage))

## Update the content of a message

Only the sender of the message and provide correctly friend_id and message_id can update the content of the message

```typescript
PUT /api/v1/user/friend/<friend_id>/message/<message_id>
authorization Bearer <token>
{
	"content": string
}
```

### Return

-   A updated UserMessage object ([UserMessage](#usermessage))

## Games

### **Create a game**

#### Input

```typescript
message: `games_create`;
payload: {
    maxDuration: 1 | 2 | 3;
    maxScore: 5 | 10 | 30 | null;
    mode: "classic" | "hardcore";
    visibility: "public" | "private";
}
```

#### Return

-   The new game object ([LocalGameInfo](#localgameinfo))
-   ```typescript
    {
    	statusCode: 400,
    	error: 'Bad request',
    	messages: string[] // describing malformed payload
    }
    ```

### **Join a game**

#### Input

```typescript
message: `games_join`
payload: {
	id: string, // Local game id
}
```

#### Return

-   The game object ([LocalGameInfo](#localgameinfo))
-   ```typescript
    {
    	statusCode: 400,
    	error: 'Bad request',
    	messages: string[] // describing malformed payload
    }
    ```
-   ```typescript
    {
    	statusCode: 404,
    	message: 'Not Found',
    	messages: ['Game not found'],
    }
    ```
-   ```typescript
    {
    	statusCode: 403,
    	error: 'Forbidden',
    	messages: ['User not invited'],
    }
    ```
-   ```typescript
    {
    	statusCode: 409,
    	error: 'Conflict',
    	messages: ['User is already in the game'],
    }
    ```

### **Quit a game**

#### Input

```typescript
message: `games_quit`
payload: {
	id: string, // Game ID
}
```

#### Return

-   The game object ([LocalGameInfo](#localgameinfo))
-   ```typescript
    {
    	statusCode: 400,
    	error: 'Bad request',
    	messages: string[] // describing malformed payload
    }
    ```
-   ```typescript
    {
    	statusCode: 404,
    	error: 'Not Found',
    	messages: ['Game not found'] |
    				['Player not found'],
    }
    ```

### **Join matchmaking**

#### Input

```typescript
message: `games_joinMatchmaking`;
payload: empty;
```

#### Return

-   `true` when you joined matchmaking

### **Invite a player in a game**

#### Input

```typescript
message: `games_invite`
payload: {
	id: string, // Local game id
	user_id: number, // ID of user to invite
}
```

#### Return

-   The user invited ([User](#user))
-   ```typescript
    {
    	statusCode: 400,
    	error: 'Bad request',
    	messages: string[] // describing malformed payload
    }
    ```
-   ```typescript
    {
    	statusCode: 404,
    	message: 'Not Found',
    	messages: ['Game not found'] |
    				['User not found'],
    }
    ```
-   ```typescript
    {
    	statusCode: 403,
    	error: 'Forbidden',
    	messages: ['Only the creator can invite'] |
    				['Game is already full'] |
    				['User is offline'], |
    				['Game is not private']
    }
    ```
-   ```typescript
    {
    	statusCode: 409,
    	error: 'Conflict',
    	messages: ['User is already in the game']
    			| ['You cannot invite yourself']
    			| ['User is already invited']
    }
    ```

### **Send new player position**

#### Input

```typescript
message: `games_playerMove`
payload: {
	id: string, // Local game id
	y: number, // The new Y position
}
```

#### Return

-   A `null` response (means everything is alright)
-   ```typescript
    {
    	statusCode: 400,
    	error: 'Bad request',
    	messages: string[] // describing malformed payload
    }
    ```
-   ```typescript
    {
    	statusCode: 404,
    	message: 'Not Found',
    	messages: ['Game not found'] |
    				['Player not found'],
    }
    ```

### **Get player games history**

#### Input

```typescript
message: `games_history`
payload: {
	id: number, // User id
}
```

#### Return

-   A game array ([Game[]](#game))
-   ```typescript
    {
    	statusCode: 400,
    	error: 'Bad request',
    	messages: string[] // describing malformed payload
    }
    ```
-   ```typescript
    {
    	statusCode: 404,
    	message: 'Not Found',
    	messages: ['User not found'],
    }
    ```

### **Get player statistics**

#### Input

```typescript
message: `games_userStats`
payload: {
	id: number, // User id
}
```

#### Return

-   A user stats object ([StatsUser](#statsuser))
-   ```typescript
    {
    	statusCode: 400,
    	error: 'Bad request',
    	messages: string[] // describing malformed payload
    }
    ```
-   ```typescript
    {
    	statusCode: 404,
    	message: 'Not Found',
    	messages: ['User not found'],
    }
    ```

### **Get leaderboards**

#### Input

```typescript
message: `games_leaderboards`;
payload: empty;
```

#### Return

-   A leaderboards object ([Leaderboards](#leaderboards))

### **Start watching a game**

#### Input

```typescript
message: `games_startWatching`
payload: {
	id: string, // Game id, optionnal if you provide a user_id
	user_id: number, // User id, optionnal if you provide a game id
}
```

#### Return

-   The local game info object ([LocalGameInfo](#localgameinfo))
-   ```typescript
    {
    	statusCode: 400,
    	error: 'Bad request',
    	messages: string[] // describing malformed payload
    }
    ```
-   ```typescript
    {
    	statusCode: 404,
    	message: 'Not Found',
    	messages: ['Game not found'],
    }
    ```

### **Stop watching a game**

#### Input

```typescript
message: `games_stopWatching`
payload: {
	id: string, // Game id, optionnal if you provide a user_id
	user_id: number, // User id, optionnal if you provide a game id
}
```

#### Return

-   The local game info object ([LocalGameInfo](#localgameinfo))
-   ```typescript
    {
    	statusCode: 400,
    	error: 'Bad request',
    	messages: string[] // describing malformed payload
    }
    ```
-   ```typescript
    {
    	statusCode: 404,
    	message: 'Not Found',
    	messages: ['Game not found'],
    }
    ```

# Websocket Events

## Users

### **New private message**

-   Event name: `users_message`
-   Data type: [UserMessage](#usermessage)

### **On profile update**

When a user related to you update his profile (a friend or someone who is in one of the channels you joined)

-   Event name: `users_update`
-   Data type: [User](#user)

### **On friendship invitation**

-   Event name: `users_friendshipInvitation`
-   Data type: [UserFriend](#userfriend)

### **On friendship acceptation**

-   Event name: `users_friendshipAccepted`
-   Data type: [UserFriend](#userfriend)

### **On friendship deletion**

When someone remove your friendship or decline your invitation

-   Event name: `users_friendshipRemoved`
-   Data type: [UserFriend](#userfriend)

### **On ban**

When someone ban you from his friends.

-   Event name: `users_banned`
-   Data type: [BannedUser](#banneduser)

### **On mute**

-   Event name: `users_muted`
-   Data type: [MutedUser](#muteduser)

## Channels

### **New channel message**

-   Event name: `channels_message`
-   Data type: [ChannelMessage](#channelmessage)

### **On channel update**

-   Event name: `channels_update`
-   Data type: [Channel](#channel)

### **On member join**

When a new member join the channel

-   Event name: `channels_join`
-   Data type: [Channel](#channel)

### **On member leave**

When a member leave the channel

-   Event name: `channels_leave`
-   Data type: [Channel](#channel)

### **On admin added**

When a member is promoted admin

-   Event name: `channels_addAdmin`
-   Data type: [Channel](#channel)

### **On admin removed**

When a member is downgraded

-   Event name: `channels_removeAdmin`
-   Data type: [Channel](#channel)

### **On member ban**

When a member is banned

-   Event name: `channels_banUser`
-   Data type: [ChannelBannedUser](#channelbanneduser)

### **On member mute**

When a member is muted

-   Event name: `channels_muteUser`
-   Data type: [ChannelMutedUser](#channelmuteduser)

### **On channel invitation**

When you receive an invitation to join a channel

-   Event name: `channels_inviteUser`
-   Data type: [ChannelInvitedUser](#channelinviteduser)

#### Example

```typescript
socket.on("channels_message", (data: any) => {
    console.log(`New message from ${data.user.username} in ${data.channel.name}: ${data.message}`);
});
```

## Games

### **Game start**

Send game information 3 seconds before the start of the game.

-   Event name: `games_start`
-   Data type: [LocalGameInfo](#localgameinfo)

### **Invitation to a game**

-   Event name: `games_invitation`
-   Data type: [LocalGameInfo](#localgameinfo)

### **Game end**

-   Event name: `games_end`
-   Data type:
    ```typescript
    	{
    		winner: {
    			user: User,
    			score: number,
    		},
    		score: number,
    		opponent_score: number,
    	}
    ```

### **New opponent position**

-   Event name: `games_opponentMove`
-   Data type:
    ```typescript
    {
        y: number;
    }
    ```

### **New score (after a goal)**

-   Event name: `games_score`
-   Data type:
    ```typescript
    	you: number, // your score
    	opponent: number, // opponent score
    ```

### **On play invitation**

-   Event name: `games_invitation`
-   Data type:
    ```typescript
    	game: LocalGameInfo,
    	inviter: User,
    ```

### **New ball position**

-   Event name: `games_ballMove`
-   Data type:
    ```typescript
    	x: number,
    	y: number
    ```

### **Watch - New creator position**

-   Event name: `games_watch_creatorMove`
-   Data type:
    ```typescript
    {
        y: number;
    }
    ```

### **Watch - New opponent position**

-   Event name: `games_watch_opponentMove`
-   Data type:
    ```typescript
    {
        y: number;
    }
    ```

### **Watch - New ball position**

-   Event name: `games_watch_ballMove`
-   Data type:
    ```typescript
    	x: number,
    	y: number
    ```

### **Watch - New score (after a goal)**

-   Event name: `games_watch_score`
-   Data type:
    ```typescript
    	creator: number, // creator score
    	opponent: number, // opponent score
    ```

### **Watch - Game end**

-   Event name: `games_watch_end`
-   Data type:
    ```typescript
    	{
    		winner: {
    			user: User,
    			score: number,
    		},
    		creator_score: number,
    		opponent_score: number,
    	}
    ```

# Objects

## WSResponse

```typescript
{
	statusCode: number, // HTTP status code
	error: string, // Relatded HTTP message
	messages: string[], // array of string describing the problem
}
```

## User

```typescript
{
	id: number,
	id42: number, // null for non-42 users
	username: string,
	displayName: string,
	status: 'online' | 'offline' | 'playing',
	elo: number,
	firstConnection: boolean,
	invitedFriends: UserFriends[],
	friendOf: UserFriend[],
	friends: User[],
	profile_picture: string,
}
```

## UserFriend

```typescript
{
	inviterId: number,
	inviter: User,

	inviteeId: number,
	invitee: User,

	accepted: boolean
}
```

## BannedUser

```typescript
{
	userId: number,
	user: User,

	bannedId: number,
	banned: User,

	until: Date
}
```

## MutedUser

```typescript
{
	userId: number,
	user: User,

	mutedId: number,
	muted: User,

	until: Date
}
```

## UserMessage

```typescript
{
	id: number,

	senderId: number,
	sender: User,

	receiverId: number,
	receiver: User,

	message: string,

	sentAt: Date
}
```

## Channel

```typescript
{
	id: number,
	code: string,
	owner: User,
	name: string,
	visibility: 'public' | 'private' | 'protected',
	admins: User[],
	members: User[],
	banned: User[],
	muted: User[],
	invited: User[],
}
```

## ChannelBannedUser

```typescript
{
	userId: number,
	user: User,

	channelId: number,
	channel: Channel,

	until: Date,
}
```

## ChannelMutedUser

```typescript
{
	userId: number,
	user: User,

	channelId: number,
	channel: Channel,

	until: Date,
}
```

## ChannelInvitedUser

```typescript
{
	userId: number,
	user: User,

	inviterId: number,
	inviter: User,

	channelId: number,
	channel: Channel,

	invited_at: Date,
}
```

## ChannelMessage

```typescript
{
	id: number,

	senderId: number,
	serder: User,

	channelId: number,
	channel: Channel,

	message: string,

	sentAt: Date,
}
```

## Game

```typescript
{
	id: number,
	visibility: 'public' | 'private',
	mode: 'classic' | 'hardcore',
	maxDuration: 1 | 2 | 3;
	maxScore: 5 | 10 | 30 | null,

	winner: User,
	winnerScore: number,

	loser: User,
	loserScore: number,
}
```

## LocalGameInfo

```typescript
{
	id: string,
	state: "waiting" | "started" | "ended" | "saved",
	startAt: number | null,
	players: Array<{
		user: User,
		score: number,
	}>,
	paddleHeight: number,
}
```

## StatsUser

```typescript
{
	user: User,
	stats: {
		games: number,
		wins: number,
		losses: number,
		winrate: number,
	},
}
```

## Leaderboards

```typescript
{
	elo: User[],
	mostPlayed: StatsUser[],
}
```

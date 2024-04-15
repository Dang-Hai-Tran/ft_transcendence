# Table of content

-   [Authentication](#authentication)
-   [Channels](#channels)
-   [Websocker Events](#websocket-events)
-   [Objects](#objects)

## Per modules

-   **Auth**
    -   [Login](#login)
    -   [Register](#register)
    -   [Switch OTP status](#switch-otp-status)
    -   [Get OTP status](#get-otp-status)
    -   [Get OTP code](#get-otp-code)
    -   [Check OTP code](#check-otp-code)
    -   [Get OTP QR code](#get-otp-qr-code)
-   **Users**
    -   [Get informations about yourself](#get-my-profile)
    -   [Get a profile avatar](#get-a-profile-avatar)
    -   [Upload a profile avatar](#upload-a-profile-avatar)
    -   [Get my profile](#get-my-profile)
    -   [Update a user](#update-user)
    -   [Invite a friend](#invite-as-friend)
    -   [Accept a friendship request](#accept-friendship-request)
    -   [Remove a friend or decline friendship request](#remove-friend-or-decline-friendship-request)
    -   [Ban a user from your friend](#ban-user)
    -   [Mute a user](#mute-user)
    -   [Send a private message](#send-a-message)
    -   [Retrieve a conversation](#get-messages)
    -   [New private message](#new-private-message)
    -   [On profile update](#on-profile-update)
    -   [On friendship invitation](#on-friendship-invitation)
    -   [On friendship acceptation](#on-friendship-acceptation)
    -   [On friendship deletion](#on-friendship-deletion)
    -   [On ban](#on-ban)
    -   [On mute](#on-mute)
-   **Channels**
    -   [Create a channel](#create-channel)
    -   [List visible channels](#list-channels)
    -   [Get a channel](#get-channel)
    -   [Update a channel](#update-channel)
    -   [Join a channel](#join-channel)
    -   [List joined channels](#list-joined-channel)
    -   [Leave a channel](#leave-channel)
    -   [Add a channel administrator](#add-channel-administrator)
    -   [Remove a channel administrator](#remove-channel-administrator)
    -   [Ban a user](#ban-user-from-channel)
    -   [Mute a user](#mute-user-from-channel)
    -   [Invite a user in a channel](#invite-user-in-channel)
    -   [Send a message in a channel](#send-message-into-channel)
    -   [Retrieve channel conversation](#get-channel-messages)
    -   [New message](#new-channel-message)
    -   [On channel update](#on-channel-update)
    -   [On member join](#on-member-join)
    -   [On member leave](#on-member-leave)
    -   [On admin added](#on-admin-added)
    -   [On admin removed](#on-admin-removed)
    -   [On member ban](#on-member-ban)
    -   [On member mute](#on-member-mute)
    -   [On channel invitation](#on-channel-invitation)
-   **Games**
    -   [Create a game](#create-a-game)
    -   [Join a game](#join-a-game)
    -   [Quit a game](#quit-a-game)
    -   [Join the matchmaking](#join-matchmaking)
    -   [Send new player position](#send-new-player-position)
    -   [Invite a user in a game](#invite-a-player-in-a-game)
    -   [Get a player games history](#get-player-games-history)
    -   [Get a player statistics](#get-player-statistics)
    -   [Get the leadreboards](#get-leaderboards)
    -   [Start watching a game](#start-watching-a-game)
    -   [Stop watching a game](#stop-watching-a-game)
    *   [Before game start](#game-start)
    *   [On game end](#game-end)
    *   [New opponent position](#new-opponent-position)
    *   [New score](#new-score-after-a-goal)
    *   [New ball position](#new-ball-position)
    *   [Watch - New creator position](#watch---new-creator-position)
    *   [Watch - New opponent position](#watch---new-opponent-position)
    *   [Watch - New ball position](#watch---new-ball-position)
    *   [Watch - New score](#watch---new-score-after-a-goal)
    *   [Watch - On game end](#watch---game-end)

# Authentication

Every routes, except `/register` and `/login` you need to provide an Bearer token in the request headers.

```
authorization: Bearer <token>
```

## Login

````typescript
POST /api/v1/auth/login
{```
	username: string,
	password: string,
	otp: string (optional)
}
````

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
	message: string
}
```

Register a user if it doesn't exist

## Switch OTP status

```typescript
POST /api/v1/auth/otp/switch
{
	username: string
}
authorization Bearer <token>
```

### Return

```typescript
{
	otpStatus: boolean
}
```

Switch OTP status: true -> false, false -> true

## Get OTP status

```typescript
GET /api/v1/auth/otp/status
authorization Bearer <token>
```

### Return

```typescript
{
	otpStatus: boolean
}
```

Get OTP status of a user

## Get OTP code

```typescript
GET /api/v1/auth/otp
authorization Bearer <token>
```

### Return

```typescript
{
	otp: string
}
```

Get OTP of a user

## Check OTP code

```typescript
POST /api/v1/auth/otp/check
{
	username: string,
	otp: string
}
authorization Bearer <token>
```

### Return

```typescript
{
	message: string
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

```
{
	updated user's data
}
```

## Get a profile avatar

```
GET /api/v1/profile/me/avatar
authorization Bearer <token>
```

### Return

-   The user's profile avatar ([UserAvatar](#useravatar))

Retrieve the user's profile avatar from backend storage

## Upload a profile avatar

```typescript
POST /api/v1/profile/me/avatar
authorization Bearer <token>
avatar: File
```

### Return

```typescript
{
	message: string
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
	message: string
}
```

Create a new channel by user. The user will be the owner of the channel and be added to the list of admins and members

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
GET /api/v1/channel/get/<channel_id>
authorization Bearer <token>
```

### Return

-   The channel object ([Channel](#channel))

## Update channel by owner

Only channel's owner can update the channel

```typescript
PUT /api/v1/channel/update/<channel_id>
authorization Bearer <token>
{
	"name": string, // optionnal
	"visibility": 'public' | 'private', // optionnal
	"password": string // optionnal
}
```

### Return

```typescript
{
	... updated channel data ...
}
```

Updata name, visibility or password of a channel by admin

## Add new admin by owner

Only channel's owner can add user as admin and the user must be a member of the channel and isn't already an admin of the channel

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
	message: string
}
```

## Remove admin by owner

Only channel's owner can remove user as admin. The user must be a admin of the channel

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
	message: string
}
```


## Join a channel

Every one can join a public channel. Only invited users can join a private channel. If user is banned from the channel, he can't join it. The user have to provide a password to join if the channel's password is set. The user will be added to the list of members of the channel.

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


## Ban user from channel by admin



To unban a user, simply ban the user again with a past date.

#### Input

```typescript
message: `channels_banUser`
payload: {
	id: number, // the channel id
	user_id: number,
	until: string, // ISO date of de-ban
}
```

#### Return

-   A ChannelBannedUser object ([ChannelBannedUser](#channelbanneduser))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```
    -   ```typescript
        {
        	statusCode: 403,
        	error: 'Forbidden',
        	messages: ['Only channel admins can ban users'],
        }
        ```
    -   ```typescript
        {
        	statusCode: 404,
        	error: 'Not found',
        	messages: ['Channel not found']
        			| ['User not found']
        }
        ```

### **Mute user from channel**

To unmute a user, simply mute the user again with a past date.

#### Input

```typescript
message: `channels_muteUser`
payload: {
	id: number, // the channel id
	user_id: number,
	until: string, // ISO date of de-ban
}
```

#### Return

-   A ChannelMutedUser object ([ChannelMutedUser](#channelmuteduser))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```
    -   ```typescript
        {
        	statusCode: 403,
        	error: 'Forbidden',
        	messages: ['Only channel admins can mute users'],
        }
        ```
    -   ```typescript
        {
        	statusCode: 404,
        	error: 'Not found',
        	messages: ['Channel not found']
        			| ['User not found']
        }
        ```

### **Invite user in channel**

#### Input

```typescript
message: `channels_inviteUser`
payload: {
	id: number, // the channel id
	user_id: number,
}
```

#### Return

-   A ChannelInvitedUser object ([ChannelInvitedUser](#channelinviteduser))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```
    -   ```typescript
        {
        	statusCode: 403,
        	error: 'Forbidden',
        	messages: ['Only channel admins can invite users'],
        }
        ```
    -   ```typescript
        {
        	statusCode: 404,
        	error: 'Not found',
        	messages: ['Channel not found']
        			| ['User not found']
        }
        ```
    -   ```typescript
        {
        	statusCode: 409,
        	error: 'Conflict',
        	messages: ["You can't invite yourself"]
        			| ['There is already a pending invitation']
        }
        ```

### **Send message into channel**

#### Input

```typescript
message: `channels_sendMessage`
payload: {
	id: number, // the channel id
	message: string,
}
```

#### Return

-   A ChannelMessage object ([ChannelMessage](#channelmessage))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```
    -   ```typescript
        {
        	statusCode: 403,
        	error: 'Forbidden',
        	messages: ['Only channel members can send messages'],
        			| ['You are muted in this channel']
        }
        ```
    -   ```typescript
        {
        	statusCode: 404,
        	error: 'Not found',
        	messages: ['Channel not found']
        }
        ```

### **Get channel messages**

Retrieve 200 message before the date passed.

#### Input

```typescript
message: `channels_messages`
payload: {
	id: number, // the channel id
	before: string, // ISO date
}
```

### Example

To retrieve the last 200 messages.

```typescript
socket.emit(
    "channels_messages",
    {
        id: 1,
        before: new Date().toISOString(),
    },
    (data) => {
        console.log(data); // The messages array
    }
);
```

#### Return

-   An array of ChannelMessage object ([ChannelMessage[]](#channelmessage))
-   ```typescript
    {
    	statusCode: 400,
    	error: 'Bad request',
    	messages: string[] // describing malformed payload
    }
    ```
-   ```typescript
    {
    	statusCode: 403,
    	error: 'Forbidden',
    	messages: ['Only channel members can read messages'],
    }
    ```
-   ```typescript
    {
    	statusCode: 404,
    	error: 'Not found',
    	messages: ['Channel not found']
    }
    ```

## Users

### **Get user**

#### Input

```typescript
message: `users_get`;
payload: {
    id: number; // User id
}
```

#### Return

-   The user object ([User](#user))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```

### **Update user**

#### Input

```typescript
message: `users_update`
payload: {
	id: number, // User id
	username: string, // Optionnal new username
	displayName: string, // Optionnal new username
}
```

#### Return

-   The updated user object ([User](#user))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```
    -   ```typescript
        {
        	statusCode: 403,
        	error: 'Forbidden',
        	messages: ['You can only update your own user'],
        }
        ```
    -   ```typescript
        {
        	statusCode: 404,
        	error: 'Not found',
        	messages: ['User not found'],
        }
        ```

### **Invite as friend**

#### Input

```typescript
message: `users_inviteFriend`
payload: {
	username: string, // Username of the friend to invite
}
```

#### Return

-   The new friendship object ([UserFriend](#userfriend))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```
    -   ```typescript
        {
        	statusCode: 403,
        	error: 'Forbidden',
        	messages: ['You have been banned'],
        }
        ```
    -   ```typescript
        {
        	statusCode: 404,
        	error: 'Not found',
        	messages: ['User not found'],
        }
        ```
    -   ```typescript
        {
        	statusCode: 409,
        	error: 'Conflict',
        	messages: ['There is already a pending invitation']
        				| ["You can't invite yourself"],
        				| ["You are already friends"]
        }
        ```

### **Accept friendship request**

#### Input

```typescript
message: `users_acceptFriend`
payload: {
	id: number, // Id of the user how invited the client
}
```

#### Return

-   The updated friendship object ([UserFriend](#userfriend))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```
    -   ```typescript
        {
        	statusCode: 409,
        	error: 'Conflict',
        	messages: ['Friendship already accepted'],
        }
        ```
    -   ```typescript
        {
        	statusCode: 404,
        	error: 'Not found',
        	messages: ['User not found'],
        }
        ```

### **Remove friend (or decline friendship request)**

#### Input

```typescript
message: `users_removeFriend`
payload: {
	id: number, // Id of the user how invited the client
}
```

#### Return

-   The deleted friendship object ([UserFriend](#userfriend))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```
    -   ```typescript
        {
        	statusCode: 409,
        	error: 'Conflict',
        	messages: ['Friendship not found'],
        }
        ```
    -   ```typescript
        {
        	statusCode: 404,
        	error: 'Not found',
        	messages: ['User not found'],
        }
        ```

### **Ban user**

#### Input

```typescript
message: `users_ban`
payload: {
	id: number, // Id of the user to ban
	until: string, // ISO Date of the un-ban
}
```

#### Return

-   The new user banned object ([BannedUser](#banneduser))
-   A [WSResponse](#wsresponse)
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
        	error: 'Not found',
        	messages: ['User not found'],
        }
        ```

### **Mute user**

#### Input

```typescript
message: `users_mute`
payload: {
	id: number, // Id of the user to ban
	until: string, // ISO Date of the un-ban
}
```

#### Return

-   The new user muted object ([MutedUser](#muteduser))
-   A [WSResponse](#wsresponse)
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
        	error: 'Not found',
        	messages: ['User not found'],
        }
        ```

### **Send a message**

#### Input

```typescript
message: `users_sendMessage`
payload: {
	id: number, // Id of a friend
	until: string, // Message to send
}
```

#### Return

-   The new message object ([UserMessage](#usermessage))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```
    -   ```typescript
        {
        	statusCode: 403,
        	error: 'Forbidden',
        	messages: ['You can only send messages to friends'],
        			| ['You are muted by this user']
        }
        ```
    -   ```typescript
        {
        	statusCode: 404,
        	error: 'Not found',
        	messages: ['User not found'],
        }
        ```

### **Get messages**

#### Input

```typescript
message: `users_getMessages`
payload: {
	id: number, // Id of a friend
	before: string, // ISO date
}
```

#### Return

-   An array of messages object ([UserMessage[]](#usermessage))
-   A [WSResponse](#wsresponse)
    -   ```typescript
        {
        	statusCode: 400,
        	error: 'Bad request',
        	messages: string[] // describing malformed payload
        }
        ```
    -   ```typescript
        {
        	statusCode: 403,
        	error: 'Forbidden',
        	messages: ['You can only get messages from friends'],
        }
        ```
    -   ```typescript
        {
        	statusCode: 404,
        	error: 'Not found',
        	messages: ['User not found'],
        }
        ```

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

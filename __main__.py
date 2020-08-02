import discord
import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import json

# TODO: THIS IS THE CHROME BUILD

# Discord Bot Token - Controls (ESEA Viewer#5877 Bot)
with open('token.txt') as inp:
    token = inp.readline()
client = discord.Client()

# Extension variables - chromedriver-new-options (obsolete without the extension.crx file)
# options = webdriver.ChromeOptions()
# options.add_extension('/Users/jonathanbest/Desktop/ESEA-Ranks_v1.7.crx')

# geckodriver path & variable declaration
driver_path = r'/Users/memoriuhl/PycharmProjects/ESEAAPI/chromedriver'
cd = driver_path

# Rank & League roles associated with account
rank_roles = (
    "S", "G", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D",
    "D-")

league_roles = ("OPEN","IM","MAIN","ADV","MDL")


def profile_page(alias):
    driver = webdriver.Chrome(cd)
    url = "https://play.esea.net/api/users/" + alias + "/profile"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    page_json = json.loads(soup.find("body").text)
    driver.close()
    usrl = url.replace("/profile", "")
    return page_json

# - Pulls the json page for a players basic profile info - #


def user_json(driver, usrl):
    # To use this the command must provide a username as the variable (nick)
    driver.get(usrl)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    page_json = json.loads(soup.find("body").text)
    return page_json

# - Pulls the json page for a players profile page - #


def profile_json(driver, alias):
    # To use this the command must provide a username as the variable (nick)
    url = "https://play.esea.net/api/users/" + alias + "/profile"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    page_json = json.loads(soup.find("body").text)
    usrl = url.replace("/profile", "")
    return page_json, usrl

# - Pulls the json page for a players pug stats - #


def pug_json(driver, usrl):
    # To use this the command must provide a username as the variable (nick)
    url = usrl + "/stats?filters[type_scopes]=pug&filters[period_types]=months"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    page_json = json.loads(soup.find("body").text)
    return page_json

# - Pulls the json page for a players league stats - #


def league_json(driver, usrl):
    # To use this the command must provide a username as the variable (nick)
    url = usrl + \
        "/stats?filters[type_scopes]=league&filters[period_types]=months"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    page_json = json.loads(soup.find("body").text)
    return page_json


def recent_json(driver, usrl):
    url = usrl + "/matches?page_size=5&page=1"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    page_json = json.loads(soup.find("body").text)
    return page_json


def matchpage_json(driver, match_id):
    url = "https://play.esea.net/api/match/" + match_id + "/overview"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    page_json = json.loads(soup.find("body").text)
    return page_json


def searchpage_load(driver, message, alias):

    return  # Put match find info here


def match_stats(matchpage):
    # Team_1 - Stats Grab
    players = []
    rounds_played = []
    frags = []
    deaths = []
    ADR = []
    RWS = []
    msgf = []

    team_name = [matchpage['data']['teams']['team_1']['name'],
                 matchpage['data']['teams']['team_2']['name']]
    team_score = [matchpage['data']['teams']['team_1']['score'],
                  matchpage['data']['teams']['team_2']['score']]
    formatted_message = team_name[0] + ' - ' + str(team_score[0]) + '\n'
    # team_name[1] = matchpage['data']['teams']['team_2']['name']
    users_A = len(matchpage['data']['teams']['team_1']['players'])
    users_B = len(matchpage['data']['teams']['team_2']['players'])
    users_T = users_A + users_B
    for c in range(users_T):
        x = c
        if x >= users_A:
            i = 2
            x = x - users_A
        else:
            i = 1
        if(c == users_A):
            formatted_message = formatted_message + \
                team_name[1] + ' - ' + str(team_score[1]) + '\n'
        players.append(matchpage['data']['teams']['team_{0}'.format(
            i)]['players'][x]['user']['alias'])
        rounds_played.append(matchpage['data']['teams']["team_{0}".format(
            i)]['players'][x]['stats'][0]['rounds_played'])
        frags.append(matchpage['data']['teams']["team_{0}".format(
            i)]['players'][x]['stats'][0]['frags'])
        deaths.append(matchpage['data']['teams']["team_{0}".format(
            i)]['players'][x]['stats'][0]['deaths'])
        ADR.append(matchpage['data']['teams']["team_{0}".format(
            i)]['players'][x]['stats'][0]['adr'])
        RWS.append(matchpage['data']['teams']["team_{0}".format(
            i)]['players'][x]['stats'][0]['rws'])
        # print(team_name[i-1], players[c], frags[c], deaths[c], ADR[c], RWS[c], rounds_played[c])
        name_spaces = ' ' * (17 - len(players[c]))
    # Alias char lim is 17

        msgf.append(name_spaces + players[c] + " | " + str(frags[c]) + ' - ' + str(
            deaths[c]) + ' - ' + str(ADR[c]) + ' - ' + str(RWS[c]) + ' - ' + str(rounds_played[c]))
        formatted_message = formatted_message + (msgf[c] + '\n')
    print(formatted_message)

    return formatted_message

# - Checks to see if user is using command on self, or other user - #


def search_method(message, member):
    if len(message.content.split(' ')) > 1:
        alias = message.content.split(' ')[1]
        print(alias, "used a command")
    else:
        try:
            user = str(member.nick)
            if (user == "None"):
                user = str(member).split("#")[0]
            alias = user
            print(alias, "used a command")
        except AttributeError:
            alias = discord_alias(member)
            print(alias)
    if(alias == "pug"):
        alias = int(1)
    return alias


def discord_alias(member):
    try:
        user = str(member.nick)
        if (user == "None"):
            user = str(member).split("#")[0]
        alias = user
        print(alias, "used a command")
    except AttributeError:
        alias = discord_alias(member)
        print(alias)
    return user


def teaminfo_JSON(teamid, driver):
    # Above we obtained the most similar team's ID.
    # Below we obtain the JSON page for the team page.

    team_url = teamid.replace("net", "net/api")
    driver.get(team_url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    teampage_json = json.loads(soup.find("body").text)

    # Below we obtain the JSON page for the team stats.
    stats_url = team_url + '/stats'
    driver.get(stats_url)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    statspage_json = json.loads(soup.find("body").text)

    return teampage_json, statspage_json


@client.event
# each message should request specific pages, they should have methods of accessing these webpages #
async def on_message(message):
    cmd = message.content.startswith
    member = message.author
    cmd_channel = ['']  # - commands usable in these channels
    user_role = ['']   # - these roles can use the commands

    if cmd('.'):
        alias = search_method(message, member)

        if cmd('.esea'):
            alias = discord_alias(message.author)

            try:
                profilepage = profile_page(alias)
                print('profile found')
                # The above acquires the json of the ESEA user's profile page #
                esearank = profilepage['data']['rank']['current']

                try:
                    esealeague = (profilepage['data']['league'][0]['league']['type']).upper()
                    print(esealeague)
                except:
                    esealeague = 'none'

                if (len(esearank) > 2):
                    await message.channel.send("No Rank Found")
                else:
                    new_role = discord.utils.get(
                        message.guild.roles, name=esearank)
                    league_role = discord.utils.get(
                        message.guild.roles, name=esealeague)

                    user = message.author

                    for x in range(len(rank_roles)):
                        role = discord.utils.get(
                            message.guild.roles, name=rank_roles[x])
                        await user.remove_roles(role)
                    await user.add_roles(new_role)

                    if (esealeague != 'none'):
                        for y in range(len(league_roles)):
                            Lrole = discord.utils.get(
                                message.guild.roles, name=league_roles[y])
                            await user.remove_roles(Lrole)
                        await user.add_roles(league_role)

                    await message.channel.send("Rank & League Added")
                    print('Rank & League Added')

            except TypeError:
                print("TypeError: Discord username has no correlating ESEA profile")
                await message.channel.send("Error, try changing nickname to ESEA profile name!")

        # TODO: Make a nice CSS message in discord to format the data nicely
        if cmd('.stats'):
            if(alias == int(1)):
                alias = discord_alias(member)
                print('\n'+alias+'\n')
                driver = webdriver.Chrome(cd)
                profilepage, usrl = profile_json(driver, alias)
                # checks users most recent matches
                recentmatches = recent_json(driver, usrl)
                # grabs match ID from the most recent match
                match_id = str(recentmatches['data'][0]['id'])
                # grabs the json of the match overview
                matchjson = matchpage_json(driver, match_id)
                driver.close()
                # grabs stats of all players and prepares it for a message
                discord_stats = match_stats(matchjson)
                await message.channel.send('```' + discord_stats + '```')
            else:
                driver = webdriver.Chrome(cd)
                profilepage, usrl = profile_json(driver, alias)
                userinfo = user_json(driver, usrl)
                pugstats = pug_json(driver, usrl)
                leaguestats = league_json(driver, usrl)
                driver.close()

                status = userinfo['data']['tier']
                name = userinfo['data']['alias']
                karma = userinfo['data']['karma']
                rank = profilepage['data']['rank']['current']
                team = profilepage['data']['league'][0]['team']['name']
                league = profilepage['data']['league'][0]['league']['name']
                # data.server_stats.stats[12].value
                pug_adr = pugstats['data']["server_stats"]['stats'][12]['value']
                # data.server_stats.stats[14].value
                pug_rws = pugstats['data']["server_stats"]['stats'][14]['value']
                # data.server_stats.stats[12].value
                lea_adr = leaguestats['data']["server_stats"]['stats'][12]['value']
                # data.server_stats.stats[14].value
                lea_rws = leaguestats['data']["server_stats"]['stats'][14]['value']

                # final_team = 'lol\n\r **NAME | ** {0} [{1}]\n **TEAM | ** {2} [{3}]\n **PUG |** ADR: {4} RWS: {5}\n **LEAGUE |** ADR: {6} RWS: {7}\n'.format(name, rank, team, league, pug_adr, pug_rws, lea_adr, lea_rws)
                final_team = '```  NAME | {0} [{1}]\n  TEAM | {2} [{3}]\n   PUG | ADR: {4} RWS: {5}\nLEAGUE | ADR: {6} RWS: {7}\n```'.format(
                    name, rank, team, league, pug_adr, pug_rws, lea_adr, lea_rws)
                # final_team = '\n' + 'NAME' + ' '*(8) + '|\n' + "TEAM" + ' '*(8) + '|\n' + "PUG" + ' '*(5) + '|\n' + "LEAGUE" + ' '*(2) + '|'
                await message.channel.send(final_team)

        # TODO :
        # - Looks at a users most recent game and posts stats of each player. links to the game page #
        if cmd('.pug'):
            print('\n'+alias+'\n')
            driver = webdriver.Chrome(cd)
            profilepage, usrl = profile_json(driver, alias)
            # checks users most recent matches
            recentmatches = recent_json(driver, usrl)
            # grabs match ID from the most recent match
            match_id = str(recentmatches['data'][0]['id'])
            # grabs the json of the match overview
            matchjson = matchpage_json(driver, match_id)
            driver.close()
            # grabs stats of all players and prepares it for a message
            discord_stats = match_stats(matchjson)
            await message.channel.send('```' + discord_stats + '```')

        # TODO :
        # - Searches for teams with similar names and picks the one closest to the string given
        # - finds available stats for each member of the team, as well as their current record
        if cmd('.team'):
            driver = webdriver.Chrome(cd)
            search_url = "https://play.esea.net/index.php?s=search&source=teams&query=" + \
                alias.replace(
                    ' ', '%20') + "&source=teams&filters%5Bgame_id%5D=25&fields%5Bname%5D=1"
            driver.get(search_url)
            results = driver.execute_script(
                "return document.getElementsByClassName('result-container').length")

            # Below is the method used to find teams based on search and similarity.
            if results == 0:    # If no results
                await message.channel.send('**No Teams Found**')
            else:               # If there are results
                team_type = []
                # Search the teams in the list and add them to a list.
                for i in range(1, results + 1):
                    y = i - 1
                    yuh = driver.find_element_by_xpath(
                        '//*[@id="search-default"]/section[3]/div[' + str(i) + ']/h2').text
                    print(yuh)
                    team_type.append(yuh)
                    if team_type[y].count('League') >= 1:   # Check only league teams
                        league_team_name = (driver.find_element_by_xpath(
                            '//*[@id="search-default"]/section[3]/div[' + str(i) + ']/a[1]')).text
                        if (str(league_team_name.lower()).count(alias.lower()) >= 1):
                            teamid = (driver.find_element_by_xpath(
                                '//*[@id="search-default"]/section[3]/div[' + str(i) + ']/a[1]')).get_attribute('href')

                            teampage_json, statspage_json = teaminfo_JSON(
                                teamid, driver)

                            driver.close()

                            # List of variables from a team's stats list:
                            player = []
                            frags = []
                            assists = []
                            deaths = []
                            plants = []
                            defuses = []
                            threeKs = []
                            fourKs = []
                            fiveKs = []
                            onevones = []
                            onevtwos = []
                            hsp = []
                            rp = []
                            adr = []
                            fpr = []
                            rws = []
                            msgf = []
                            team_stats = []
                            final_msg = ''
                            print("starting for-loop")

                            team_name = teampage_json['data']['name']
                            team_tag = teampage_json['data']['tag']
                            team_id = teampage_json['data']['id']
                            team_picture = teampage_json['data']['avatar_full_url']
                            team_league = teampage_json['data']['league']['league']['name']
                            team_W = str(
                                teampage_json['data']['league']['record']['win'])
                            team_L = str(
                                teampage_json['data']['league']['record']['loss'])
                            team_T = str(
                                teampage_json['data']['league']['record']['tie'])
                            team_record = '{0}-{1}-{2}'.format(
                                team_W, team_L, team_T)

                            await message.channel.send((('```{0} ({1}) | {2} ({3})\r```').format(team_name, team_tag, team_league, team_record)))
                            print(('{0} ({1}) | {2} ({3})\r').format(
                                team_name, team_tag, team_league, team_record))
                            rows = int(
                                len(statspage_json['data']['team_1']['players']))

                            for x in range(rows):
                                player.append(
                                    str(statspage_json['data']['team_1']['players'][x]['user']['alias']))
                                frags.append(
                                    int(statspage_json['data']['team_1']['players'][x]['stats'][0]['frags']))
                                deaths.append(
                                    int(statspage_json['data']['team_1']['players'][x]['stats'][0]['deaths']))
                                hsp.append(
                                    float(statspage_json['data']['team_1']['players'][x]['stats'][0]['hsp']))
                                adr.append(
                                    float(statspage_json['data']['team_1']['players'][x]['stats'][0]['adr']))
                                fpr.append(
                                    float(statspage_json['data']['team_1']['players'][x]['stats'][0]['fpr']))
                                rws.append(
                                    float(statspage_json['data']['team_1']['players'][x]['stats'][0]['rws']))
                                rp.append(
                                    int(statspage_json['data']['team_1']['players'][x]['stats'][0]['rp']))
                                player_spaces = ' ' * (17 - len(player[x]))

                                team_stats.append(('{0} {1} | {2} {3} {4} {5} {6} {7} {8}'.format(
                                    player_spaces, player[x], frags[x], deaths[x], hsp[x], adr[x], fpr[x], rws[x], rp[x])))

                                final_msg = final_msg + team_stats[x] + '\n'
                            print(final_msg)

        if cmd(''):
            return


async def on_member_join(driver, member):
    alias = str(member).split("#")[0]
    try:
        profilepage = profile_page(alias)
        print('profile found')
        # The above acquires the json of the ESEA user's profile page #
        esearank = profilepage['data']['rank']['current']

        try:
            esealeague = (profilepage['data']['league'][0]['league']['type']).upper()
            print(esealeague)
        except:
            esealeague = 'none'


        if (len(esearank) > 2):
            await member.send("Welcome " + alias + "! Please set your nickname to your ESEA profile name!")
        else:
            rankrole = discord.utils.get(member.guild.roles, name=esearank)
            leaguerole = discord.utils.get(member.guild.roles, name=esealeague)
            user = member
            await user.add_roles(rankrole, esealeague)
            await user.send("Roles Added!")
    except TypeError:
        print("TypeError: Discord username has no correlating ESEA profile")
        await member.send("Error, try changing nickname to ESEA profile name!")
    driver.close()

client.run(token)

import urllib2
import re
from bs4 import BeautifulSoup
import time

def getMatchStats(matchObj):
    stats={}
    stats['runs'] = int(re.match(r'\s*(\d+).*',matchObj.group(1)).group(1))
    overs= map(int,re.match(r'\s*\((\S+)\)\s*',matchObj.group(2)).group(1).split("."))
    stats['over'] =overs[0]
    stats['ball'] = 0 if len(overs) == 1 else overs[1]
    stats['runRate'] = stats['runs'] / float(6*stats['over']+stats['ball'])*6
    return stats

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
url="http://www.google.com/search?q=ipl+today&rlz=1C5CHFA_enIN874IN874&oq=ipl+tod&aqs=chrome.0.69i59j69i57j0l5j69i60.4431j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11k7x_h0dd;5;/m/03b_lm1;dt;fp;1;;"

html = opener.open(url).read()

parser = BeautifulSoup(html,features="html5lib")
teams=parser.findAll('div',{'class':'BNeawe s3v9rd AP7Wnd lRVwie'})[:3]


hour,min = time.localtime().tm_hour , time.localtime().tm_min
obj = re.compile(r'.*>(.*)</div>$')
team1, team2 = map(lambda team: obj.match(team.__str__()).group(1),teams[1:])
matchNum  =obj.match(parser.find('div',{'class':'BNeawe tAd8D AP7Wnd'}).__str__()).group(1)

print('\n')
if hour < 19 or (hour == 19 and min<30):
    time = '%s , 7.30 PM' % (re.findall('<span.*>(.*)</span>,',teams[0].__str__())[0])
    print(matchNum+' : '+time)
    print('\n')
    print "%s VS %s\n" % (team1, team2)
else:
    print(matchNum)
    print('\n')
    print "%s VS %s\n" % (team1, team2)
    scoreParser = re.compile(r'<div.*AP7Wnd"\s*>(.*)<span.*>\s*(.*)\s*</span>\s*</div>')
    score1,score2 = map(lambda score:scoreParser.match(score.__str__()),parser.findAll('div',{'class':'BNeawe deIvCb AP7Wnd'})[1:3])
    print '%s : %s\n' % (team1,score1.group(1)+score1.group(2))
    print '%s : %s\n' % (team2,score2.group(1)+score2.group(2) if score2 else 'Yet to bat')
    
    teams1Stats = getMatchStats(score1)
    
    if not score2:
        if teams1Stats['over'] < 20:
            print 'Current Run Rate : %f \n' % (teams1Stats['runRate'])
            print 'Predicted score : %d \n' % (teams1Stats['runRate']*20)
        else:
            print '%s need %d runs to win \n' % (team2,teams1Stats['runs']+1)
    else:
        teams2Stats =getMatchStats(score2)

        if teams2Stats['over'] == 20:
            winner = team2 if teams2Stats['runs'] > teams1Stats['runs'] else team1
            print '%s won the match !! \n' % (winner)
        else:
            target = teams1Stats['runs']+1
            print '%s need %d runs to win with %d runs left\n' % (team2,target,target-teams2Stats['runs'])
            print 'Current Run Rate : %f \n' % (teams2Stats['runRate'])
            print 'Required Run Rate : %f \n' % ((target - teams2Stats['runs'])/float(120-(6*teams2Stats['over'])-teams2Stats['ball'])*6)
#nrr1,nrr2


print('\n')

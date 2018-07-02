import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

global cookie
global headers

headers = {

        'Authorization': 'Token token={{}}', 					# Fill
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1;\
                                   Nexus 6 Build/MOB31H)',
}

cookie = {'_Backpack_session': '{{}}'} 						# Fill

def getAllDiscussionIDs(courseID):

	"""
		courseID : ID of the backpack course
		returns : list of discussionIDs, list of discussionWights

	"""

	print "Getting all discussion IDs for course %d" % (int(courseID))

	import requests
	import json

	global cookie
	global headers

	url = 'https://www.usebackpack.com/api/alldiscussions/' + str(courseID)

	r = requests.post(url, cookies = cookie,
						   headers = headers,\
						   verify = False)
	
	r.connection.close()
	content = r.content

	content = content.replace("nil", "0")
	content = content.replace("true", "1")
	content = content.replace("false", "-1")

	jsonContent = json.loads(content)

	allIDs = jsonContent['discussionids']
	allWeights = jsonContent['discussionweights']

	return allIDs, allWeights

def getDiscussion(discussionID):

	"""
		discussionID : ID of the backpack discussion
		returns : dict of the response

		if discussion not found/error, returns {'status', 'error'}
	"""

	print "Getting discussion with id %d" % (int(discussionID))

	import requests
	import json

	global cookie
	global headers

	url = 'https://www.usebackpack.com/api/showdiscussion/' + str(discussionID)

	r = requests.post(url, cookies = cookie,
						   headers = headers,\
						   verify = False)
	
	r.connection.close()
	content = r.content

	content = content.replace('\n', '')
	content = content.replace('\r', '')

	jsonContent = json.loads(content)

	return jsonContent

def getCourseID(discussionID):

	"""
		discussionID : ID of the backpack discussion
		returns : courseID of the discussion

	"""

	print "Getting course id of discussion with id %d" % (int(discussionID))

	jsonContent = getDiscussion(discussionID)

	return jsonContent['course']

def getAllDiscussion(courseID):
	
	"""
		courseID : ID of the backpack course
		returns : dict {'discussionID' : jsonContent of the discussion}

	"""
	print "Getting all discussions of course id %d" % (int(courseID))

	allIDs, _ = getAllDiscussionIDs(courseID)

	allContent = {}

	for id_ in allIDs:
		discussionContent = getDiscussion(id_)
		allContent[id_] = discussionContent

	return allContent

def getCourseInfo(courseId):

    url = 'https://www.usebackpack.com/api/courseinfo/' + str(courseId)
    r = requests.post(url, cookies = cookie,
                           headers = headers,\
                           verify = False)
    content = r.content
    content = ''.join([c for c in content if ord(c) >= 31 and ord(c) < 128])
    content = content.replace('\\', '')
    
    contentJson = json.loads(content)
    return contentJson

def getUserInfoAndCourses(userID):
    
    url = 'https://www.usebackpack.com/api/userinfo/' + str(userID)

    r = requests.post(url, cookies = cookie,
                           headers = headers,\
                           verify = False)
    
    if r.status_code == 200:
        
        content = r.content
        contentJson = json.loads(content.split('number_of_discussions')[0][:-9] + '}')
        userName = contentJson['first_name'] + ' ' + contentJson['last_name']
        userEmail = contentJson['email']
        print "Fetching courses for ", userName, userEmail

        upperCounter, lowerCounter = 0, 0
        contentLines = content.split()

        for lineIndex in range(len(contentLines)):    
            if 'notifications' in contentLines[lineIndex]:
                upperCounter = lineIndex
            elif 'upcomingdeadlines' in contentLines[lineIndex]:
                lowerCounter = lineIndex
                break

        allCourses = []

        for line in contentLines[upperCounter : lowerCounter]:
            if line[0] == '"' and line[-2:] == ':{':
                allCourses.append(line[1:-3])

        return userName, userEmail, allCourses
    
    else:
        print 'No user exists for', userID
        return False

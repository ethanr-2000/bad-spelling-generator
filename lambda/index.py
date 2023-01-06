import re
import json

from helpers.spell_bad import spell_bad
from helpers.util import load_pronunciation_dictionary, load_isle

isleDict = load_isle()
pd = load_pronunciation_dictionary()

def handler(event, context):
  request = json.loads(event['body'])

  words_list = re.findall(r"[\w']+|[.,!?; ]", request['text'])
  response = {"words": []}
  for word in words_list:
      if re.match(r"[.,!?; ]", word):
          response['words'].append({'badlySpelled': [word]})
          continue
      bad_spell_response = spell_bad(word, isleDict, pd)
      response['words'].append(bad_spell_response)

  return {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': true,
      'Access-Control-Allow-Headers': "Origin, X-Requested-With, Content-Type, Accept"
    },
    'body': json.dumps(response)
  }

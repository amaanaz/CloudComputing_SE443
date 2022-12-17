import json
import urllib3


http = urllib3.PoolManager()
get_wrong_req = http.request('GET', 'https://reqres.in/api/unknown/23')
get_req = http.request('GET', 'https://reqres.in/api/unknown/1')

# checking for respinse form the server
if get_req.status != 200:
    print('Error: ', get_req.status)
    print('Please Try again !')
elif get_req.status == 400:
    print('Error: ', get_req.status)
    print('Bad Request!')
elif get_req.status == 404:
    print('Error: ', get_req.status)
    print('Not Found!')

else:
    print(get_req.status)

    # check if data is string
    if type(get_req.data) != str:
        print('It is not a string')

    # decode the data to be a json format.
    data = json.loads(get_req.data.decode('utf-8'))

    print('Name:', data['data']['name'])
    print('Year:', data['data']['year'])
    print('Pantone', data['data']['pantone_value'])

# create a post request.
post_req = http.request('POST', 'https://reqres.in/api/users',
                        body=json.dumps(
                            {'Name': 'UnjustKey',
                             'Motto': 'Lost in the Woods'}
                        ),
                        headers={'Content-Type': 'application/json'})

if (post_req.status == 201):
    print("\n", post_req.status, "\n Sent Data:")
sent_data = json.loads(post_req.data.decode('utf-8'))
print(" Name", sent_data['Name'])
print(" Motto", sent_data['Motto'])

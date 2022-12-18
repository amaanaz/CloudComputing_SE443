import sys
import docker
import time

start_time = time.time()
client = docker.from_env()
client.swarm.leave(force=True)

try:
    print("Swarm Creation")
    client.swarm.init()
    print("Swarm Id: ", client.swarm.attrs['ID'])
    print("Swarm Name: ", client.swarm.attrs['Spec']['Name'])
    print("Swarm creation time: ", client.swarm.attrs['CreatedAt'])

    print("\nCreating the network")
    client.networks.create("se443_test_net", driver="overlay", scope="global", ipam=docker.types.IPAMConfig(
        pool_configs=[docker.types.IPAMPool(subnet='10.10.10.0/24')]))
    for network in client.networks.list():
        if network.name == "se443_test_net":
            print("Network Id: ", network.id)
            print("Network Name: ", network.name)
            print("Network creation time: ", network.attrs['Created'])

    print("\nCreating the broker service")
    client.services.create("eclipse-mosquitto", name="broker",  restart_policy=docker.types.RestartPolicy(
        condition="any"), networks=["se443_test_net"]).scale(3)
    time.sleep(5)
    print("Broker serv Id: ", client.services.list()[0].id)
    print("Broker serv Name: ", client.services.list()[0].name)
    print("Broker serv creation time: ",
          client.services.list()[0].attrs['CreatedAt'])
    print("Broker serv Replicas: ", client.services.list()[
        0].attrs['Spec']['Mode']['Replicated']['Replicas'])

    print("\nCreating the subscriber service")
    client.services.create("efrecon/mqtt-client", name="subscriber",  restart_policy=docker.types.RestartPolicy(
        condition="any"), networks=["se443_test_net"], command='sub -h host.docker.internal -t AU -v').scale(3)
    time.sleep(5)
    print("Subscriber serv id: ", client.services.list()[0].id)
    print("Subscriber serv name: ", client.services.list()[0].name)
    print("Subscriber serv creation time: ",
          client.services.list()[0].attrs['CreatedAt'])
    print("Service replicas: ", client.services.list()[
        0].attrs['Spec']['Mode']['Replicated']['Replicas'])

    print("\nCreating the publisher service")
    client.services.create("efrecon/mqtt-client", name="publisher",  restart_policy=docker.types.RestartPolicy(
        condition="any"), networks=["se443_test_net"], command='pub -h host.docker.internal -t AU -m "<Hey Its Amaan Zubairi ; Id : 200226>"').scale(3)
    time.sleep(5)
    print("Publisher serv id: ", client.services.list()[0].id)
    print("Publisher serv name: ", client.services.list()[0].name)
    print("Publisher serv creation time: ",
          client.services.list()[0].attrs['CreatedAt'])
    print("Service replicas: ", client.services.list()[
        0].attrs['Spec']['Mode']['Replicated']['Replicas'])

    print("\nRunning for 60 seconds")

    # wait for 60 seconds
    while True:
        if time.time() - start_time > 60:
            print("60 seconds done -")
            print("\nRemoving services")

            # Removing Publisher Service
            print("\nRemoving Publisher service")
            client.services.get("publisher").remove()
            print("Publisher removed")

            # Removing Subcriber Service
            print("\nRemoving Subscriber service")
            client.services.get("subscriber").remove()
            print("Subscriber removed")

            # Removing Broker Service
            print("\nRemoving Broker service")
            client.services.get("broker").remove()
            print("Broker removed")

            # Removing Network
            print("\nRemoving network")
            client.networks.get("se443_test_net").remove()
            print("Network removed")

            # Removing Swarm
            print("\nRemoving swarm")
            client.swarm.leave(force=True)
            print("Swarm removed")
            break

except Exception as e:
    print("Error on line {}".format(
        sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    print("Error: ", e)

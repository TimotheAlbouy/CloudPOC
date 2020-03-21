from client.client_middleware import ClientMiddleware

client = ClientMiddleware()

client.create_variable("salary_alice", 2500)
client.create_variable("salary_bob", 1500)
client.create_variable("salary_charlie", 0)

alice_lt_bob = client.compare_variables("salary_alice", "salary_bob")
print("Alice's salary is lower than Bob's: ", alice_lt_bob)

client.update_variable("salary_bob", 3000)
print("Bob's salary is updated.")

alice_lt_bob = client.compare_variables("salary_alice", "salary_bob")
print("Alice's salary is lower than Bob's: ", alice_lt_bob)

client.add_variables("salary_alice", "salary_bob", "salary_charlie")
salary_charlie = client.get_variable("salary_charlie")[1]
print("Charlie's salary: ", salary_charlie)

client.delete_variable("salary_alice")
client.delete_variable("salary_bob")
client.delete_variable("salary_charlie")
print("All variables are deleted.")

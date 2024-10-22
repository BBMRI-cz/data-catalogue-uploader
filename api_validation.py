import molgenis.client


session = molgenis.client.Session("http://147.251.124.190:8080/api/")
session.login("admin", "admin")

table = session.get("fair-genomes_Analysis")
print(table)
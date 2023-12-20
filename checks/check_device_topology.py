from collections import defaultdict

from infrahub.checks import InfrahubCheck


class InfrahubCheckDeviceTopology(InfrahubCheck):

    query = "check_device_topology"

    def validate(self):

        device_roles = {}
        expected_roles = {}

        for device in self.data["data"]["InfraDevice"]["edges"]:
            role = device["node"]["role"]["value"]
            site = device["node"]["site"]["node"]["name"]["value"]

            if site not in device_roles:
                device_roles[site] = {}

            if role in device_roles:
                device_roles[site][role] += 1
            else:
                device_roles[site][role] = 1

        for element in self.data["data"]["InfraTopologyElement"]["edges"]:
            expected_role = element["node"]["name"]["value"]
            expected_roles[expected_role] = element["node"]["amount"]["value"]

        for site in device_roles.items():
            for role in device_roles[site].items():
                if device_roles[site][role] != expected_roles[role]:
                    self.log_error(
                        message=f"{site} does not have expected amount of {role} ({device_roles[site][role]}/{expected_roles[role]})",
                        object_id=role,
                        object_type="role",
                    )

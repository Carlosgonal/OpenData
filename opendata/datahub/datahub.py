
from datapackage import Package


def main():
    package = Package('https://datahub.io/core/country-list/datapackage.json')

    # get list of all resources:
    print(package)
    resources = package.descriptor['resources']
    resourceList = [resources[x]['name'] for x in range(0, len(resources))]
    print(resourceList)

    # print all tabular data(if exists any)
    resources = package.resources
    for resource in resources:
        if resource.tabular:
            print(resource.read())


if __name__ == "__main__":
    main()

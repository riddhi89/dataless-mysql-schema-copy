import subprocess

# initialize the parameters
SOURCE_HOSTNAME = 'source.database.com'
SOURCE_USERNAME = 'sourceuser'
SOURCE_PASSWORD = 'sourcedbpassword'
SOURCE_SCHEMAS = ['test-db-1', 'test-db-2', 'test-db-3']
TARGET_HOSTNAME = 'target.database.com'
TARGET_USERNAME = 'targetuser'
TARGET_PASSWORD = 'targetdbpassword'

dataless_backup_cmd = (
    'mysqldump -h {} -P 3306 -u {} -p{} '
    '--no-data --compress --databases {} '
    '--routines=0 --triggers=0 --events=0 --set-gtid-purged=OFF'
)
dataless_import_cmd = (
    'mysql -h {} -P 3306 -u {} -p{}'
)

for schema in SOURCE_SCHEMAS:
    print("Migrating structure for schema {}...".format(schema))

    dataless_backup = dataless_backup_cmd.format(
        SOURCE_HOSTNAME,
        SOURCE_USERNAME,
        SOURCE_PASSWORD,
        schema
    )
    dataless_import = dataless_import_cmd.format(
        TARGET_HOSTNAME,
        TARGET_USERNAME,
        TARGET_PASSWORD
    )

    import_process = subprocess.Popen(
        dataless_import.split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=-1
    )
    backup_process = subprocess.Popen(
        dataless_backup.split(),
        stdout=import_process.stdin,
        stderr=subprocess.PIPE,
        bufsize=-1
    )

    result, err = backup_process.communicate()

    if 'Got error' in err:
        raise Exception("Problem copying schema structure for {}. "
                        "Details:{}".format(schema, err))

    print("Finished migrating structure for schema {}".format(schema))

print("Completed migrating all schemas!")

# ❄️ snowflake-permissions ❄️

This is a script for managing permissions in Snowflake. Permissions are defined in `users.yaml` and `roles.yaml`. Running the `snowflake.ipynb` will read those permissions, check them against what's currently in Snowflake, and update the permissions to match the configuration files.


## How the configuration files work
These scripts define users, roles, and the relationships between them. Note that this script will create new roles, but it won't create new users. Users need to be created manually before adding them to `users.yaml`.

##### User configuration
```
- name: [ Username in Snowflake ]
  properties:
    display_name: [ Display name ]
    first_name: [ First name ]
    last_name: [ Last name ]
    email: [ Email of user ]
    disable_mfa: [ TRUE/FALSE. If user needs MFA to log in. ]
    comment: [ Description of user ]
    default_warehouse: [ Default warehouse for user ]
    default_namespace: [ Default database for user ]
    default_role: [ Default role for user ]
  roles: 
    - foo  ## List of roles the user has
    - bar  ## is associated with.
```
##### Role configuration
```
-   name: [ Name of role ]
    description: [ Description of role ]
    parent_role: [ Role that inherits permissions of this role. If no custom role should be the parent, set to sysadmin. ]
    warehouses: 
        - foo  ## List of warehouses that the role
        - bar  ## has access too.
    read_from:
        - db1.schema_foo  ## List of schemas the role can read from. Use 
        - db2.schema_bar  ## db_name.* to grant read access to all 
        - db3.*           ## schemas in that database.
    create_in:
        - db4.schema_baz  ## List of schemas the role can create in. Use 
        - db5.schema_qux  ## db_name.* to grant read access to all 
        - db6.*           ## schemas in that database.
    owner_of:
        - db7.*  ## List of schemas the role can read from and create in in. Use 
        - db8.*  ## db_name.* to grant access to all schemas in that database.
```
Note that schemas must exist prior to granting permissions. Also note that permissions must be granted by schema. While Snowflake allow permissions to be set on individual tables, this script requires all table in the same schema to have the same permissions.

from olp.utils import patch_models
from .backend import TestBackendBasic
from .utils import TestAssignPerm, TestHasPerm, TestRemovePerm, \
    TestRemoveAllPermissions, TestRemovePermNotSet, TestGetObjsForUser

patch_models()

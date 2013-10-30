from olp.utils import patch_models
from .backend import TestBackendBasic
from .utils import TestAssignPerm, TestHasPerm, TestRemovePerm, TestRemovePermNotSet, TestGetObjsForUser

patch_models()

static PyMethodDef CoreMethods[] = {
    {"init", init, METH_VARARGS, "Init Function"},
    {"simulate", simulate, METH_VARARGS, "Simulate Function"},
    {"memfree", memfree, METH_VARARGS, "Memory Free Function"},
    {NULL, NULL, 0, NULL}    /* Sentinel */
};


static struct PyModuleDef core = {
    PyModuleDef_HEAD_INIT,
    "core",    /* name of module */
    "doc",    /* module documentation */
    -1,    /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    CoreMethods
};


PyMODINIT_FUNC
PyInit_core(void)
{
    return PyModule_Create(&core);
}


class TestSaver:

    saved_tests = set()

    def __init__(self, filePath):
        self.file = open(filePath, "w");
        self.file.write('test_input\n');
        self.file.write('-----------' + '\n');

    #private member functions
    def __write_to_file(self, testcase):
            self.file.write(testcase + '\n');


    #public member functions
    def save_test_case(self, testcase):
            self.saved_tests.add(testcase);

    def export_to_file(self):
        for test in self.saved_tests:
            self.__write_to_file(test);

        self.file.close();
from conans import ConanFile, CMake, tools


class EfswConan(ConanFile):
    name = "efsw"
    version = "1.1.0"
    license = "MIT"
    author = "Jim Klo <jim@klofamily.org>"
    url = "https://github.com/SpartanJ/efsw"
    description = "efsw is a C++ cross-platform file system watcher and notifier"
    topics = ("inotify", "fsevents", "kqueue", "filewatcher")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/SpartanJ/efsw.git")
        self.run(f"cd efsw && git checkout -b {self.version}", ignore_errors=True) 
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("efsw/CMakeLists.txt", "project (efsw)",
                              '''project (efsw)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="efsw")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("**.h", dst="include", src="efsw/include")
        self.copy("**.hpp", dst="include", src="efsw/include")
        self.copy("**.hpp", dst="include", src="src/efsw")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["efsw"]


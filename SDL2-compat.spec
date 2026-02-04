#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	SDL2 compatibility layer that uses SDL3 behind the scenes
Name:		SDL2-compat
Version:	2.32.64
Release:	1
License:	Zlib (BSD-like)
Group:		Libraries
Source0:	http://www.libsdl.org/release/sdl2-compat-%{version}.tar.gz
# Source0-md5:	67f7e69cfacc25c51496f2702ce32654
Patch0:		SDL2-config.patch
URL:		http://www.libsdl.org/
BuildRequires:	SDL3-devel
BuildRequires:	automake
BuildRequires:	cmake >= 3.0
BuildRequires:	pkgconfig >= 1:0.7
BuildRequires:	rpmbuild(macros) >= 1.742
# runtime (dlopened) dep actually but require it for convenience
%requires_ge_to	SDL3 SDL3-devel
Provides:	SDL2 = %{version}-%{release}
%{?_isa:Provides:	SDL2%{_isa} = %{version}-%{release}}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SDL (Simple DirectMedia Layer) is a library that allows you portable,
low level access to a video framebuffer, audio output, mouse, and
keyboard. It can support both windowed and DGA modes of XFree86, and
it is designed to be portable - applications linked with SDL can also
be built on Win32 and BeOS.

This package provides SDL2 compatibility layer that uses SDL3 behind
the scenes.

%package devel
Summary:	SDL2-compat Header files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
SDL2-compat header files.

%package static
Summary:	SDL2-compat static libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
SDL2-compat static libraries.

%prep
%setup -q -n sdl2-compat-%{version}
%patch -P0 -p1

%build
install -d build
cd build
%cmake .. \
	%{cmake_on_off static_libs SDL2COMPAT_STATIC} \
	-DSDL2COMPAT_TESTS:BOOL=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT \

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BUGS.md COMPATIBILITY.md LICENSE.txt README.md
%attr(755,root,root) %{_libdir}/libSDL2-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSDL2-2.0.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sdl2-config
%attr(755,root,root) %{_libdir}/libSDL2.so
%attr(755,root,root) %{_libdir}/libSDL2-2.0.so
%{_libdir}/libSDL2_test.a
%{_libdir}/libSDL2main.a
%{_includedir}/SDL2
%{_aclocaldir}/sdl2.m4
%{_pkgconfigdir}/sdl2-compat.pc
%{_libdir}/cmake/SDL2

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libSDL2.a
%endif

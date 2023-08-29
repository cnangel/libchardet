%define _tmppath %{_topdir}/BUILDROOT
%define prefix_flag	%(if test -z $prefix ; then echo 0; else echo 1; fi;)

Name: libchardet
Version: 0.0.9
Release: 1%{?dist}

Summary: a library for charset detector
License: GPLv3
Group: Application/Systems
Url: http://www.mozilla.org/projects/intl/chardet.html
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -u -n)
%if %{prefix_flag}
Prefix: %_prefix
%endif

%define PACKAGE_HOME %{_datadir}/libchardet

Packager: Cnangel <cnangel@gmail.com>

%description
%{name}(Charset detector) in Mozilla is a XPCOM component which receive bytes as incoming data and base on the bytes of data "guess" what the charset of the data is and report it to the caller.

%package devel
Summary: Header files, libraries for %{name}.
Group: %{group}
Requires: %{name} = %{version}-%{release} 

%description devel
This package contains the header files and static libraries for %{name}.
If you like to develop programs using %{name}, you will need to install %{name}-devel.

%prep
%setup -q

%build
./autogen.sh
%configure
make %{?_smp_mflags}
make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post
if test "x$RPM_INSTALL_PREFIX0" != "x" ; then
    %{__perl} -pi -e"s|/usr|$RPM_INSTALL_PREFIX0|" $RPM_INSTALL_PREFIX0/%{_lib}/pkgconfig/libcharset.pc
    %{__perl} -pi -e"s|^libdir='[^\']*'|libdir='$RPM_INSTALL_PREFIX0/%{_lib}'|" $RPM_INSTALL_PREFIX0/%{_lib}/libchardet.la
fi

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_bindir}

%files devel
%defattr(-,root,root,-)
%{_includedir}
%{_libdir}/*.a
%{_libdir}/*.so
%if 0%{?rhel} < 8 || 0%{?fedora} < 28
%exclude %{_libdir}/*.la
%endif
%{_libdir}/pkgconfig/libchardet.pc

%changelog
* Tue Aug 29 2023 Cnangel <cnangel@gmail.com> 0.9.0-1
- support fedora38.
- add pc file.
- support github workflow.
* Tue Mar 23 2010 Cnangel <cnangel@gmail.com> 0.8.0-1
- create spec file.

# -fin-

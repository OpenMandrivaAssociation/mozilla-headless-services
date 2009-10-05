Name: mozilla-headless-services
Summary: DBus Mozilla Services library
Group: System Environment/Desktop
Version: 0.10.3
License: LGPL
URL: http://www.moblin.org
Release: %mkrel 1
Source0: http://git.moblin.org/cgit.cgi/%{name}/snapshot/%{name}-%{version}.tar.bz2
Patch0: %{name}-0.10.2-makefile.patch
Patch1: %{name}-0.10.3-includes.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: libglib2-devel
BuildRequires: libdbus-glib-devel
BuildRequires: libGConf2-devel
BuildRequires: xulrunner-headless-devel
BuildRequires: gnome-common
BuildRequires: gtk-doc

Requires: xulrunner-headless

%description
Mozilla Headless Services provides a DBus interface to
various Mozilla services, such as history, bookmarking
and preferences.

%package devel

Summary: Mozilla Headless Services development environment
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Header files and libraries for Mozilla Headless Services

%prep
%setup -q 
%patch0
%patch1
perl -pi -e 's,^./configure.*,,' ./autogen.sh

%build
./autogen.sh
%configure2_5x --enable-gnome-proxy
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/%{_datadir}/doc/%{name}-%{version}
for f in `ls %{buildroot}/%{_datadir}/doc/`; do
	if [ -f %{buildroot}/%{_datadir}/doc/$f ]; then
		mv %{buildroot}/%{_datadir}/doc/$f %{buildroot}/%{_datadir}/doc/%{name}-%{version}
	fi
done

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%exclude %{_libdir}/*.la
%{_libdir}/*.so.*
%{_libexecdir}/mhs-service
%{_datadir}/dbus-1/services/*.service

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/mhs-1.0/*
%{_libdir}/pkgconfig/*.pc

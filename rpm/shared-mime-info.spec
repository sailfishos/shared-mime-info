Name:       shared-mime-info
Summary:    Shared MIME information database
Version:    1.2
Release:    1
Group:      System/Libraries
License:    GPLv2
URL:        http://freedesktop.org/Software/shared-mime-info
Source0:    %{name}-%{version}.tar.xz
Source101:  shared-mime-info-rpmlintrc
Patch0:     text-x-vnote.patch
Patch1:     0001-Add-audio-x-opus-ogg-mime-type.patch
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  gawk
BuildRequires:  intltool
BuildRequires:  perl-XML-Parser >= 2.31-16

%description
This is the freedesktop.org shared MIME info database.

Many programs and desktops use the MIME system to represent the types of
files. Frequently, it is necessary to work out the correct MIME type for
a file. This is generally done by examining the file's name or contents,
and looking up the correct MIME type in a database.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description devel
Development files for %{name}


%prep
%setup -q -n %{name}-%{version}/shared-mime-info

# text-x-vnote.patch
%patch0 -p1

# 0001-Add-audio-x-opus-ogg-mime-type.patch
%patch1 -p1

%build
NOCONFIGURE=1 ./autogen.sh
%configure

make

%install
rm -rf %{buildroot}
%make_install

find $RPM_BUILD_ROOT%{_datadir}/mime -type d \
| sed -e "s|^$RPM_BUILD_ROOT|%%dir |" > %{name}.files
find $RPM_BUILD_ROOT%{_datadir}/mime -type f -not -path "*/packages/*" \
| sed -e "s|^$RPM_BUILD_ROOT|%%ghost |" >> %{name}.files

## remove these bogus files
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/locale/*

%docs_package

%post
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :

%files -f %{name}.files
%defattr(-,root,root,-)
%{_bindir}/update-mime-database
%dir %{_datadir}/mime/
%{_datadir}/mime/packages/freedesktop.org.xml

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/*.pc


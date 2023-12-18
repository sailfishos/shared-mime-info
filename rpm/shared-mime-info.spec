Name:       shared-mime-info
Summary:    Shared MIME information database
Version:    2.4
Release:    1
License:    GPLv2+
URL:        https://github.com/sailfishos/shared-mime-info
Source0:    %{name}-%{version}.tar.xz
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  gettext
BuildRequires:  meson

Patch1:     0001-Add-text-x-vnote-.vnt.patch

%description
This is the freedesktop.org shared MIME info database.

Many programs and desktops use the MIME system to represent the types of
files. Frequently, it is necessary to work out the correct MIME type for
a file. This is generally done by examining the file's name or contents,
and looking up the correct MIME type in a database.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
%description devel
Development files for %{name}

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}

%description doc
Man page for update-mime-database from %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/shared-mime-info

%build

%meson
%meson_build

%install
%meson_install

find $RPM_BUILD_ROOT%{_datadir}/mime -type d \
| sed -e "s|^$RPM_BUILD_ROOT|%%dir |" > %{name}.files
find $RPM_BUILD_ROOT%{_datadir}/mime -type f '!' -path "*/packages/*" \
| sed -e "s|^$RPM_BUILD_ROOT|%%ghost |" >> %{name}.files

## remove these bogus files
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/locale/*

%post
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :

%files -f %{name}.files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/update-mime-database
%{_datadir}/mime/packages/freedesktop.org.xml
%{_datadir}/gettext/its/shared-mime-info.its
%{_datadir}/gettext/its/shared-mime-info.loc

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/*.pc

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/update-mime-database.*

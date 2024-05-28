# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.32
# 

Name:       mosh

# >> macros
# << macros

Summary:    Mobile Shell
Version:    1.4.0
Release:    0
Group:      Applications
License:    GPLv3
URL:        https://mosh.org/
Source0:    %{name}-%{version}.tar.gz
Source1:    99-mosh-firewall.conf
Source100:  mosh.yaml
Source101:  mosh-rpmlintrc
Requires:   openssh-clients
Requires:   openssl
Requires:   perl(IO::Socket::IP)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(ncursesw)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  protobuf-compiler
BuildRequires:  protobuf-devel
BuildRequires:  libutempter-devel

%description
Mosh is a remote terminal application that supports:
  - intermittent network connectivity,
  - roaming to different IP address without dropping the connection, and
  - intelligent local echo and line editing to reduce the effects
    of "network lag" on high-latency connections.

%if "%{?vendor}" == "chum"
Type: console-application
PackagedBy: nephros
Categories:
  - Shell
  - RemoteAccess
Custom:
  Repo: https://github.com/mobile-shell/mosh
  PackagingRepo: https://github.com/sailfishos-chum/mosh
PackageIcon: https://raw.githubusercontent.com/mobile-shell/mobile-shell.github.io/master/mosh-chrome.png
Screenshots:
  - https://raw.githubusercontent.com/mobile-shell/mobile-shell.github.io/master/mosh.png
%endif


%package server
Summary:    Mobile Shell Server
Group:      Applications
Requires(post): systemd
Requires(postun): systemd

%description server
This provides the server part of mosh. Typically not needed on a phone.

SECURITY NOTE: This will install a firewall rule that allows incoming
connections on UDP ports 60000-60010 while on Wifi.
Take care that no other apps are listening on that port range while on an untrusted network!
Edit or remove /etc/connman/firewall.d/99-mosh-firewall.conf to disable this.

Mosh is a remote terminal application that supports:
  - intermittent network connectivity,
  - roaming to different IP address without dropping the connection, and
  - intelligent local echo and line editing to reduce the effects
    of "network lag" on high-latency connections.

%if "%{?vendor}" == "chum"
Title: mosh Server
PackagedBy: nephros
Categories:
  - System
  - Shell
  - Network
  - RemoteAccess
Custom:
  Repo: https://github.com/mobile-shell/mosh
  PackagingRepo: https://github.com/sailfishos-chum/mosh
PackageIcon: https://raw.githubusercontent.com/mobile-shell/mobile-shell.github.io/master/mosh-chrome.png
Screenshots:
  - https://raw.githubusercontent.com/mobile-shell/mobile-shell.github.io/master/mosh.png
%endif


%prep
%setup -q -n %{name}-%{version}/upstream

# >> setup
# << setup

%build
# >> build pre
# protoc wants CXX 14 or later
export CXXFLAGS="$CXXFLAGS -std=c++14"
# << build pre

%reconfigure --disable-static \
    --enable-client \
    --enable-server \
    --enable-completion

make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
# install a firewall rules file:
install -d %{buildroot}%{_sysconfdir}/connman/firewall.d/
install -m 644 %SOURCE1 %{buildroot}%{_sysconfdir}/connman/firewall.d/
# do not package documentation:
rm -rf %{buildroot}%{_docdir}
rm -rf %{buildroot}%{_mandir}
# fix perl shebang:
printf 'setting shebang for perl interpreter to #!%s\n' %{__perl}
find %{buildroot}/%{_bindir} -type f -exec sed -i '1s=^#!/usr/bin/\(perl\|env perl\)[5]\?=#!%{__perl}=' {} +

# << install post

%post server
# >> post server
# Package install: reload the firewall
if [ $1 -eq 1 ] ; then
systemctl try-restart connman.service >/dev/null 2>&1 || :
fi
# << post server

%postun server
# >> postun server
# Package install: reload the firewall
if [ $1 -eq 0 ] ; then
systemctl try-restart connman.service >/dev/null 2>&1 || :
fi
# << postun server

%files
%defattr(-,root,root,-)
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-client
%config %{_sysconfdir}/bash_completion.d/%{name}*
# >> files
# << files

%files server
%defattr(-,root,root,-)
%{_bindir}/%{name}-server
%config(noreplace) %{_sysconfdir}/connman/firewall.d/99-mosh-firewall.conf
# >> files server
# << files server

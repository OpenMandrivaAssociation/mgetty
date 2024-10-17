%define SENDFAX_UID 78
%define ltstgt 20211229

# PIE is broken on s390 (#868839, #872148)
%ifnarch s390 s390x
%global _hardened_build 1
%endif

Summary:	A getty replacement for use with data and fax modems
Name:		mgetty
Version:	1.2.1
Release:	1.%{ltstgt}.0
Source0:	ftp://mgetty.greenie.net/pub/mgetty/source/1.2/mgetty-%{version}.tar.xz
Source2:	logrotate.mgetty
Source3:	logrotate.sendfax
Source4:	logrotate.vgetty
Source5:	logrotate.vm
Source6:	vgetty@.service
Source7:	mgetty@.service

Patch0: mgetty-1.2.1-config.patch
Patch1: mgetty-1.2.1-policy.patch
Patch2: mgetty-1.2.1-system-gsm.patch
Patch4: mgetty-1.1.25-voiceconfig.patch
Patch5: mgetty-1.2.1-issue.patch
Patch6: mgetty-1.1.31-issue-doc.patch
Patch7: mgetty-1.2.1-helper.patch
Patch8: mgetty-1.2.1-mktemp.patch
Patch9: mgetty-1.2.1-unioninit.patch
Patch11: mgetty-1.2.1-helper2.patch
Patch12: mgetty-1.2.1-no-acroread.patch
Patch14: mgetty-1.2.1-sendmail_path.patch
Patch15: mgetty-1.2.1-lfs.patch
Patch16: mgetty-1.2.1-162174_tcflush.patch
Patch18: mgetty-1.1.33-bug_63843.patch
Patch19: mgetty-1.1.33-167830_tty_access.patch
Patch20: mgetty-1.2.1-167830.patch
Patch21: mgetty-1.2.1-turn.patch
Patch22: mgetty-1.2.1-time_range.patch
# man pages corrections
Patch23: mgetty-1.2.1-handle_spaces.patch
# updates info about starting vgetty tgrough systemd
Patch24: mgetty-1.1.36-man.patch
Patch25: mgetty-1.1.36-sd.patch
# patch updates makefiles, it removes hardcoded -s parameter of /usr/bin/install
# thus .debug files for all binaries will be generated properly
Patch26: mgetty-1.1.36-makefiles.patch
Patch27: mgetty-1.2.1-lockdev.patch
Patch28: mgetty-1.2.1-hardening.patch

License: GPLv2+
BuildRequires:	lockdev-devel
Buildrequires:	gsm-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(lockdev)
BuildRequires:	texinfo

Requires:	coreutils, 
Requires:	sendmail
Requires:	uucp
Requires(post): systemd
Requires(postun): systemd
URL: https://mgetty.greenie.net/

%package sendfax
Summary: Provides support for sending faxes over a modem
Requires: mgetty = %{version}
Requires: coreutils
Requires: netpbm
Requires(pre): /usr/sbin/useradd
Conflicts: hylafax+

%package voice
Summary: A program for using your modem and mgetty as an answering machine
Requires: mgetty = %{version}
Requires: sendmail
Requires(post): systemd
Requires(postun): systemd

%package viewfax
Summary: An X Window System fax viewer

%description
The mgetty package contains a "smart" getty which allows logins over a
serial line (i.e., through a modem). If you're using a Class 2 or 2.0
modem, mgetty can receive faxes. If you also need to send faxes,
you'll need to install the sendfax program.

If you'll be dialing in to your system using a modem, you should
install the mgetty package. If you'd like to send faxes using mgetty
and your modem, you'll need to install the mgetty-sendfax program. If
you need a viewer for faxes, you'll also need to install the
mgetty-viewfax package.

%description sendfax
Sendfax is a standalone backend program for sending fax files. The
mgetty program (a getty replacement for handling logins over a serial
line) plus sendfax will allow you to send faxes through a Class 2
modem.

If you'd like to send faxes over a Class 2 modem, you'll need to
install the mgetty-sendfax and the mgetty packages.

%description voice
The mgetty-voice package contains the vgetty system, which enables
mgetty and your modem to support voice capabilities. In simple terms,
vgetty lets your modem act as an answering machine. How well the
system will work depends upon your modem, which may or may not be able
to handle this kind of implementation.

Install mgetty-voice along with mgetty if you'd like to try having
your modem act as an answering machine.

%description viewfax
Viewfax displays the fax files received using mgetty in an X11 window.
Viewfax is capable of zooming in and out on the displayed fax.

%prep
%setup -q
#mv policy.h-dist policy.h
%patch0 -p1 -b .config
%patch1 -p1 -b .policy
%patch2 -p1 -b .system-gsm
rm -r voice/libmgsm
%patch4 -p1 -b .voiceconfig
%patch5 -p1 -b .issue
%patch6 -p1 -b .issue-doc
%patch7 -p1 -b .helper
%patch8 -p1 -b .mktemp
%patch9 -p1 -b .unioninit
%patch11 -p1 -b .helper2
%patch12 -p1 -b .no-acroread
%patch14 -p1 -b .sendmail_path
%patch15 -p1 -b .lfs
%patch16 -p1 -b .162174_tcflush
%patch18 -p1 -b .bug_63843
%patch19 -p1 -b .167830_tty_access
%patch20 -p1 -b .167830
%patch21 -p1 -b .turn
%patch22 -p1 -b .time_range
%patch23 -p1 -b .handle_spaces
%patch24 -p1 -b .man
%patch25 -p1 -b .sd
#%patch26 -p1 -b .makefile
%patch27 -p1 -b .lockdev
%patch28 -p1 -b .hardening

%build
%define makeflags CFLAGS="$RPM_OPT_FLAGS -Wall -DAUTO_PPP -D_FILE_OFFSET_BITS=64 -DHAVE_LOCKDEV -fno-strict-aliasing" LIBS="-llockdev" prefix=%{_prefix} spool=%{_var}/spool BINDIR=%{_bindir} SBINDIR=%{_sbindir} LIBDIR=%{_libdir}/mgetty+sendfax HELPDIR=%{_libdir}/mgetty+sendfax CONFDIR=%{_sysconfdir}/mgetty+sendfax MANDIR=%{_mandir} MAN1DIR=%{_mandir}/man1 MAN4DIR=%{_mandir}/man4 MAN5DIR=%{_mandir}/man5 MAN8DIR=%{_mandir}/man8 INFODIR=%{_infodir} ECHO='"echo -e"' INSTALL=%{__install} LDFLAGS="%{ldflags}"
make %{makeflags}
make -C voice %{makeflags}
make -C tools %{makeflags}

pushd frontends/X11/viewfax
make OPT="$RPM_OPT_FLAGS" CONFDIR=%{_sysconfdir}/mgetty+sendfax
popd

%install
mkdir -p %{buildroot}{%{_bindir},%{_infodir},%{_libdir}/mgetty+sendfax}
mkdir -p %{buildroot}{%{_mandir},%{_sbindir},/var/spool}
mkdir -p %{buildroot}%{_sysconfdir}/mgetty+sendfax

%define instflags CFLAGS="$RPM_OPT_FLAGS -Wall -DAUTO_PPP" prefix=%{buildroot}%{_prefix} spool=%{buildroot}%{_var}/spool BINDIR=%{buildroot}%{_bindir} SBINDIR=%{buildroot}%{_sbindir} LIBDIR=%{buildroot}%{_libdir}/mgetty+sendfax HELPDIR=%{buildroot}%{_libdir}/mgetty+sendfax CONFDIR=%{buildroot}%{_sysconfdir}/mgetty+sendfax MANDIR=%{buildroot}%{_mandir} MAN1DIR=%{buildroot}%{_mandir}/man1 MAN4DIR=%{buildroot}%{_mandir}/man4 MAN5DIR=%{buildroot}%{_mandir}/man5 MAN8DIR=%{buildroot}%{_mandir}/man8 INFODIR=%{buildroot}%{_infodir} ECHO='echo -e' INSTALL=%{__install}

make install %instflags
# the non-standard executable permissions are used due to security
install -m700 callback/callback %{buildroot}%{_sbindir}
# helper tests internally usage of suid - this is an intention
install -m4711 callback/ct %{buildroot}%{_bindir}

# this conflicts with efax
mv %{buildroot}%{_mandir}/man1/fax.1 %{buildroot}%{_mandir}/man1/mgetty_fax.1

# tools
make -C tools install %instflags

# voice mail extensions
mkdir -p %{buildroot}%{_var}/spool/voice/{messages,incoming}
make -C voice install %instflags
# the non-standard permissions are used due to security
install -m 600 -c voice/voice.conf-dist %{buildroot}%{_sysconfdir}/mgetty+sendfax/voice.conf

# don't ship documentation that is executable...
find samples -type f -exec chmod 644 {} \;

make -C frontends/X11/viewfax install %instflags MANDIR=%{buildroot}%{_mandir}/man1

# install logrotate control files
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d

# install unit file template for vgetty
mkdir -p %{buildroot}%{_unitdir}

install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/mgetty
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/sendfax
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/vgetty
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/vm
install -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/
install -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/
# install faxrunqd.service
install -m 0644 distro/faxrunqd.service %{buildroot}%{_unitdir}/

# remove file droppings from buildroot
rm -f %{buildroot}%{_bindir}/cutbl

# remove file conflict with netpbm:
rm -f %{buildroot}%{_bindir}/g3topbm

%post
if [ $1 -eq 1 ]; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi

%postun
%systemd_postun_with_restart mgetty@.service
exit 0

%pre sendfax
getent group fax >/dev/null || groupadd -g %SENDFAX_UID -r fax
getent passwd fax >/dev/null || useradd -r -u %SENDFAX_UID -g fax -d /var/spool/fax -s /sbin/nologin -c "mgetty fax spool user" fax

%postun sendfax
%systemd_postun_with_restart faxrunqd.service
exit 0

%post sendfax
if [ $1 -eq 1 ]; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi

%post voice
if [ $1 -eq 1 ]; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi

%postun voice
%systemd_postun_with_restart vgetty@.service
exit 0

%files
%doc BUGS ChangeLog README.1st Recommend THANKS doc/modems.db samples
%license COPYING
%{_bindir}/g3cat
%{_bindir}/g32pbm
%{_sbindir}/mgetty
%{_sbindir}/callback
%{_mandir}/man1/g32pbm.1*
%{_mandir}/man1/g3cat.1*
%{_mandir}/man4/mgettydefs.4*
%{_mandir}/man8/mgetty.8*
%{_mandir}/man8/callback.8*
%dir %{_sysconfdir}/mgetty+sendfax
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/login.config
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/mgetty.config
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/dialin.config
%config(noreplace) %{_sysconfdir}/logrotate.d/mgetty
%{_unitdir}/mgetty@.service

%files sendfax
%dir %{_var}/spool/fax
%attr(0755,fax,root) %dir %{_var}/spool/fax/incoming
%attr(0755,fax,root) %dir %{_var}/spool/fax/outgoing
%attr(0755,root,root) %{_bindir}/ct
%{_bindir}/faxq
%{_bindir}/faxrm
%{_bindir}/faxrunq
%{_bindir}/faxspool
%{_bindir}/kvg
%{_bindir}/newslock
%{_bindir}/pbm2g3
%{_bindir}/sff2g3
%{_sbindir}/faxrunqd
%{_sbindir}/sendfax
%dir %{_libdir}/mgetty+sendfax
%{_libdir}/mgetty+sendfax/cour25.pbm
%{_libdir}/mgetty+sendfax/cour25n.pbm
# helper tests internally usage of suid - this is an intention
%attr(04711,fax,root) %{_libdir}/mgetty+sendfax/faxq-helper
%{_mandir}/man1/pbm2g3.1*
%{_mandir}/man1/mgetty_fax.1*
%{_mandir}/man1/faxspool.1*
%{_mandir}/man1/faxrunq.1*
%{_mandir}/man1/faxq.1*
%{_mandir}/man1/faxrm.1*
%{_mandir}/man1/coverpg.1*
%{_mandir}/man1/sff2g3.1*
%{_mandir}/man5/faxqueue.5*
%{_mandir}/man8/faxq-helper.8*
%{_mandir}/man8/faxrunqd.8*
%{_mandir}/man8/sendfax.8*
%{_infodir}/mgetty.info.zst
%dir %{_sysconfdir}/mgetty+sendfax
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/sendfax.config
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/faxrunq.config
# sample config file doesn't use noreplace option to be installed always latest ver.
%config %{_sysconfdir}/mgetty+sendfax/faxspool.rules.sample
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/faxheader
# logrotate file name uses only sub-package name
%config(noreplace) %{_sysconfdir}/logrotate.d/sendfax
# faxrunqd unit file
%{_unitdir}/faxrunqd.service

%files voice
%doc voice/doc/* voice/Announce voice/ChangeLog voice/Readme
%dir %{_var}/spool/voice
%dir %{_var}/spool/voice/incoming
%dir %{_var}/spool/voice/messages
%{_sbindir}/vgetty
%{_bindir}/vm
%{_bindir}/pvfamp
%{_bindir}/pvfcut
%{_bindir}/pvfecho
%{_bindir}/pvffft
%{_bindir}/pvffile
%{_bindir}/pvffilter
%{_bindir}/pvfmix
%{_bindir}/pvfnoise
%{_bindir}/pvfreverse
%{_bindir}/pvfsine
%{_bindir}/pvfspeed
%{_bindir}/rmdfile
%{_bindir}/pvftormd
%{_bindir}/rmdtopvf
%{_bindir}/pvftovoc
%{_bindir}/voctopvf
%{_bindir}/pvftolin
%{_bindir}/lintopvf
%{_bindir}/pvftobasic
%{_bindir}/basictopvf
%{_bindir}/pvftoau
%{_bindir}/autopvf
%{_bindir}/pvftowav
%{_bindir}/wavtopvf
%{_mandir}/man1/zplay.1*
%{_mandir}/man1/pvf.1*
%{_mandir}/man1/pvfamp.1*
%{_mandir}/man1/pvfcut.1*
%{_mandir}/man1/pvfecho.1*
%{_mandir}/man1/pvffile.1*
%{_mandir}/man1/pvffft.1*
%{_mandir}/man1/pvfmix.1*
%{_mandir}/man1/pvfreverse.1*
%{_mandir}/man1/pvfsine.1*
%{_mandir}/man1/pvfspeed.1*
%{_mandir}/man1/pvftormd.1*
%{_mandir}/man1/pvffilter.1*
%{_mandir}/man1/pvfnoise.1*
%{_mandir}/man1/rmdtopvf.1*
%{_mandir}/man1/rmdfile.1*
%{_mandir}/man1/pvftovoc.1*
%{_mandir}/man1/voctopvf.1*
%{_mandir}/man1/pvftolin.1*
%{_mandir}/man1/lintopvf.1*
%{_mandir}/man1/pvftobasic.1*
%{_mandir}/man1/basictopvf.1*
%{_mandir}/man1/pvftoau.1*
%{_mandir}/man1/autopvf.1*
%{_mandir}/man1/pvftowav.1*
%{_mandir}/man1/wavtopvf.1*
%{_mandir}/man8/vgetty.8*
%dir %{_sysconfdir}/mgetty+sendfax
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/voice.conf
# logrotate file name uses only sub-package name
%config(noreplace) %{_sysconfdir}/logrotate.d/vgetty
%config(noreplace) %{_sysconfdir}/logrotate.d/vm
%{_unitdir}/vgetty@.service

%files viewfax
%doc frontends/X11/viewfax/C* frontends/X11/viewfax/README
%{_bindir}/viewfax
%dir %{_libdir}/mgetty+sendfax
%{_libdir}/mgetty+sendfax/viewfax.tif
%{_mandir}/man1/viewfax.1*

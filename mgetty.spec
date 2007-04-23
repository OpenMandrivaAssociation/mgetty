%define name 	mgetty
%define version 1.1.35
%define Date Feb22
%define release %mkrel 1

Summary:	A getty replacement for use with data and fax modems
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://mgetty.greenie.net/pub/mgetty/source/1.1/%{name}%{version}-%{Date}.tar.gz
Source1:	ftp://mgetty.greenie.net/pub/mgetty/source/1.1/%{name}%{version}-%{Date}.tar.gz.asc
URL:		http://mgetty.greenie.net/
Patch0:		mgetty-1.1.14-config.patch
Patch1:		mgetty-1.1.5-makekvg.patch
Patch2:		mgetty-1.1.14-policy.patch
Patch3:		mgetty-1.1.5-strip.patch
Patch4:		mgetty-1.1.14-echo.patch
Patch5:		mgetty-1.1.14-logrotate.patch
Patch8:		mgetty-1.1.35-noroot.patch
Patch9:		mgetty-1.1.21-linkman.patch

Patch12:	mgetty-1.1.30-64bit-fixes.patch
Patch13:	mgetty-1.1.35-force_detect.patch
Patch14:	mgetty-1.1.30-mktemp.patch
Requires:	libgr-progs netpbm
License:	GPL
Group:		Communications
BuildRequires:	groff-for-man
BuildRequires:	gccmakedep
BuildRequires:	imake
BuildRequires:	libxext-devel
BuildRequires:	rman
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	texinfo
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package	sendfax
Summary:	Provides support for sending faxes over a modem
Requires:	mgetty = %{version}-%{release}
Conflicts:	hylafax
PreReq:		rpm-helper
Group:		Communications

%package	voice
Summary:	A program for using your modem and mgetty as an answering machine
Requires:	mgetty = %{version}-%{release}
Group:		Communications

%package	viewfax
Summary:	An X Window System fax viewer
Requires:	mgetty = %{version}-%{release}
Group:		Communications

%package	contrib
Summary:	User contributed stuff that comes with %{name}
Group:		Communications
AutoReqProv:	no

%description
The mgetty package contains a "smart" getty which allows logins over a
serial line (i.e., through a modem).  If you're using a Class 2 or 2.0
modem, mgetty can receive faxes.  If you also need to send faxes, you'll
need to install the sendfax program.

If you'll be dialing in to your system using a modem, you should install
the mgetty package.  If you'd like to send faxes using mgetty and your
modem, you'll need to install the mgetty-sendfax program.  If you need a
viewer for faxes, you'll also need to install the mgetty-viewfax package.

%description	sendfax
Sendfax is a standalone backend program for sending fax files.  The
mgetty program (a getty replacement for handling logins over a serial
line) plus sendfax will allow you to send faxes through a Class 2 modem.

If you'd like to send faxes over a Class 2 modem, you'll need to install
the mgetty-sendfax and the mgetty packages.

%description	voice
The mgetty-voice package contains the vgetty system, which enables
mgetty and your modem to support voice capabilities.  In simple terms,
vgetty lets your modem act as an answering machine.  How well the system
will work depends upon your modem, which may or may not be able to handle
this kind of implementation.

Install mgetty-voice along with mgetty if you'd like to try having your
modem act as an answering machine.

%description	viewfax
Viewfax displays the fax files received using mgetty in an X11 window.
Viewfax is capable of zooming in and out on the displayed fax.

If you're installing the mgetty-viewfax package, you'll also need to
install mgetty.

%description	contrib

The contents of the contrib directory that comes with %{name}.

%prep
%setup -q
cp policy.h-dist policy.h
%patch0 -p1 -b .config
%patch1 -p1 -b .makekvg
%patch2 -p1
%patch3 -p1 -b .strip
%patch4 -p1 -b .echo
%patch5 -p1
# new texinfo much stricter about xrefs
%patch8 -p1 -b .noroot
%patch9 -p1

%patch12 -p1 -b .64bit-fixes
%patch13 -p1 -b .force_detect
%patch14 -p1 -b .mktemp

%build
%make
# 1.1.28-2mdk yves - ugly hack to have correct info dir
echo -e "\nSTART-INFO-DIR-ENTRY\n* mgetty: (mgetty).       A getty replacement use with data and fax modems.\nEND-INFO-DIR-ENTRY\n" >> doc/mgetty.info

cd voice
%make

cd ../frontends/X11/viewfax
xmkmf
make depend
%make CDEBUGFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/spool -p $RPM_BUILD_ROOT/sbin
make prefix=$RPM_BUILD_ROOT/usr spool=$RPM_BUILD_ROOT/var/spool \
	CONFDIR=$RPM_BUILD_ROOT/etc/mgetty+sendfax install
install -m700 callback/callback $RPM_BUILD_ROOT/usr/sbin
install -m4711 callback/ct $RPM_BUILD_ROOT/usr/bin
strip $RPM_BUILD_ROOT/usr/bin/newslock

mv $RPM_BUILD_ROOT/usr/sbin/mgetty $RPM_BUILD_ROOT/sbin

# this conflicts with efax
mv $RPM_BUILD_ROOT/usr/man/man1/fax.1 $RPM_BUILD_ROOT/usr/man/man1/mgetty_fax.1

# voice mail extensions
cd voice
mkdir -p $RPM_BUILD_ROOT/var/spool/voice 
mkdir -p $RPM_BUILD_ROOT/var/spool/voice/messages
mkdir -p $RPM_BUILD_ROOT/var/spool/voice/incoming

make prefix=$RPM_BUILD_ROOT/usr spool=$RPM_BUILD_ROOT/var/spool \
	CONFDIR=$RPM_BUILD_ROOT/etc/mgetty+sendfax install

mv $RPM_BUILD_ROOT/usr/sbin/vgetty $RPM_BUILD_ROOT/sbin
install -m 600 -c voice.conf-dist $RPM_BUILD_ROOT/etc/mgetty+sendfax/voice.conf
cd -
find samples -type f -exec chmod 644 {} \;

cd frontends/X11/viewfax
%{makeinstall_std} BINDIR=%{_bindir} HELPDIR=%{_prefix}/lib/mgetty+sendfax MANDIR=/usr/man/man1 install.man
cd -

mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 0644 logrotate.mgetty $RPM_BUILD_ROOT/etc/logrotate.d/mgetty
install -m 0644 logrotate.sendfax $RPM_BUILD_ROOT/etc/logrotate.d/sendfax

#move the man pages
mkdir -p $RPM_BUILD_ROOT/usr/share
mv $RPM_BUILD_ROOT/usr/man $RPM_BUILD_ROOT/usr/share
#move the info page
#mkdir $RPM_BUILD_ROOT/usr/share
mv $RPM_BUILD_ROOT/usr/info $RPM_BUILD_ROOT/usr/share

# yves - 1.1.26-4mdk - doc with good perm
find doc -type f -exec chmod 644 {} \;
chmod -f 0644 BUGS

rm -f $RPM_BUILD_ROOT/usr/bin/g3topbm

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{name}.info

%postun
if [ $1 = 0 ]; then
  %{__rm} -fr /var/log/mgetty.log*
fi
%_remove_install_info %{name}.info

%pre sendfax
%_pre_useradd fax %{_var}/spool/fax /bin/sh

%postun sendfax
%_postun_userdel fax
if [ $1 = 0 ]; then
  %{__rm} -fr /var/log/sendfax.log*
fi

%files
%defattr(-,root,root)
%doc ChangeLog README.1st THANKS TODO Recommend FTP samples/*
%doc doc/mgetty.ps doc/mgetty.dvi doc/mgetty.texi  doc/fhng-codes doc/modems.db
%doc BUGS doc/*.txt
%attr(755,root,root) /sbin/mgetty
%{_mandir}/man8/mgetty.8*
%{_mandir}/man8/callback.8*
%{_mandir}/man8/faxrunqd.8*
%{_mandir}/man4/mgettydefs.4*
%{_infodir}/mgetty.info*
%dir %{_sysconfdir}/mgetty+sendfax
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/mgetty+sendfax/login.config
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/mgetty+sendfax/mgetty.config
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/mgetty+sendfax/dialin.config
%config(noreplace) %{_sysconfdir}/logrotate.d/mgetty


%files sendfax
%defattr(-,root,root)

%attr(755,fax,fax) %dir %{_var}/spool/fax
%attr(755,fax,fax) %dir %{_var}/spool/fax/incoming
%attr(755,fax,fax) %dir %{_var}/spool/fax/outgoing
#%attr(755,fax,fax) %dir %{_var}/spool/fax/outgoing/locks

%{_bindir}/kvg
%{_bindir}/newslock
%{_bindir}/g3cat
%{_bindir}/g32pbm
%{_bindir}/pbm2g3
%{_bindir}/sff2g3
%{_bindir}/faxspool
%attr(755,root,root) %{_bindir}/faxrunq
%{_bindir}/faxq
%{_bindir}/cutbl
%{_bindir}/faxrm
%attr(755,root,root) %{_bindir}/ct
%attr(755,root,root) %{_sbindir}/sendfax
%attr(755,root,root) %{_sbindir}/faxrunqd
%attr(755,root,root) %{_sbindir}/callback
%dir	%{_prefix}/lib/mgetty+sendfax
%{_prefix}/lib/mgetty+sendfax/cour25.pbm
%{_prefix}/lib/mgetty+sendfax/cour25n.pbm
%attr(4711,fax,fax) %{_prefix}/lib/mgetty+sendfax/faxq-helper
%{_mandir}/man1/g32pbm.1*
%{_mandir}/man1/pbm2g3.1*
%{_mandir}/man1/g3cat.1*
%{_mandir}/man1/mgetty_fax.1*
%{_mandir}/man1/faxspool.1*
%{_mandir}/man1/faxrunq.1*
%{_mandir}/man1/faxq.1*
%{_mandir}/man1/faxrm.1*
%{_mandir}/man1/coverpg.1*
%{_mandir}/man1/sff2g3.1*
%{_mandir}/man5/faxqueue.5*
%{_mandir}/man8/faxq-helper.8*
%{_mandir}/man8/sendfax.8*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/mgetty+sendfax/sendfax.config
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/mgetty+sendfax/faxrunq.config
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/faxheader
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/faxspool.rules.sample
%config(noreplace) %{_sysconfdir}/logrotate.d/sendfax

%files voice
%defattr(-,root,root)
%dir %{_var}/spool/voice
%dir %{_var}/spool/voice/incoming
%dir %{_var}/spool/voice/messages

%attr(755,root,root) /sbin/vgetty
%{_bindir}/vm
%{_bindir}/pvfamp
%{_bindir}/pvfcut
%{_bindir}/pvfecho
%{_bindir}/pvffile
%{_bindir}/pvffilter
%{_bindir}/pvfnoise
%{_bindir}/pvffft
%{_bindir}/pvfmix
%{_bindir}/pvfreverse
%{_bindir}/pvfsine
%{_bindir}/pvfspeed
%{_bindir}/pvftormd
%{_bindir}/rmdtopvf
%{_bindir}/rmdfile
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
%{_mandir}/man1/pvffilter.1*
%{_mandir}/man1/pvffft.1*
%{_mandir}/man1/pvfmix.1*
%{_mandir}/man1/pvfnoise.1*
%{_mandir}/man1/pvfreverse.1*
%{_mandir}/man1/pvfsine.1*
%{_mandir}/man1/pvfspeed.1*
%{_mandir}/man1/pvftormd.1*
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
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/mgetty+sendfax/voice.conf

%files viewfax
%defattr(-,root,root)
%doc frontends/X11/viewfax/C* frontends/X11/viewfax/README
%{_bindir}/viewfax
%dir %{_prefix}/lib/mgetty+sendfax
%{_prefix}/lib/mgetty+sendfax/viewfax.tif
%{_mandir}/man1/viewfax.1x.*

%files contrib
%defattr(644,root,root,755)
%doc contrib/*


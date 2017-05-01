from pathlib import Path
import tempfile
from django.db import models
from django.utils.translation import ugettext as _


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Source(models.Model):
    title = models.CharField(_('Título'), max_length=150)
    video = models.FileField()
    transcript = models.FileField(_('Transcripción'))
    video_url = models.URLField(blank=True, null=True)
    transcript_url = models.URLField(blank=True, null=True)

    @property
    def text(self):
        return Path(self.transcript).read_text('utf8')


class Remix(models.Model):
    title = models.CharField(_('Título'), max_length=150)
    script = models.TextField(_('Guión del remix'))
    dump = models.TextField(_('Json del remix'))
    video = models.FileField(blank=True, null=True, editable=False)
    sources = models.ManyToManyField('Source', blank=True, null=True,
                                     editable=False)

    @property
    def script_file(self):
        _, temp = tempfile.mkstemp(suffix='.txt', text=True)
        Path(temp).write_text(self.script, 'utf8')
        return temp


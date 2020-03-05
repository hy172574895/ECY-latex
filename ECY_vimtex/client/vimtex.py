import lib.scope as scope_
import lib.vim_or_neovim_support as vim_lib

# the class must be named as 'Operate'
class Operate(scope_.Event):
    def __init__(self, source_name):
        scope_.Event.__init__(self, source_name)
        self.has_taxlab = None
        self.taxlab_path = None

    def _using_taxlab(self):
        if self.has_taxlab is None:
            self.has_taxlab = vim_lib.GetVariableValue('g:has_vimtex')
        return self.has_taxlab

    def _get_taxlab_path(self):
        if self.taxlab_path is None:
            self.taxlab_path = vim_lib.GetVariableValue('g:ECY_vimtex_texlab_path')
        return self.taxlab_path

    def OnBufferEnter(self):
        msg = {}
        msg['UseTablab'] = self._using_taxlab()
        if self._using_taxlab():
            msg['TexlabCMD'] = self._get_taxlab_path()
        return self._pack(msg, 'OnBufferEnter')

    def DoCompletion(self):
        msg = {}
        msg['TriggerLength'] = self._trigger_len
        msg['ReturnMatchPoint'] = self._is_return_match_point

        msg['UseTablab'] = self._using_taxlab()
        if self._using_taxlab():
            msg['TexlabCMD'] = self._get_taxlab_path()
        else:
            try:
                msg['Candidates'] = vim_lib.CallEval('ECY_vimtex#GetCandidate()')
            except:
                msg['Candidates'] = []
        return self._pack(msg, 'DoCompletion')

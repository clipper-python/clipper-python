
%ignore operator std::complex<float>;
%ignore operator std::complex<double>;
%include "../clipper/core/hkl_datatypes.h"

namespace clipper
{
namespace datatypes
{
%extend Flag_bool {
#ifdef PYTHON_PROPERTIES
  bool _get_flag()
#else
  bool get_flag()
#endif
  {
    bool theFlag = self->flag();
    return theFlag;
  }
#ifdef PYTHON_PROPERTIES
  void _set_flag(bool theFlag)
#else
  void set_flag(bool theFlag)
#endif
  {
    self->flag() = theFlag;
  }

  clipper::datatypes::Flag_bool copy()
  {
    clipper::datatypes::Flag_bool ret;
    ret = *self;
    return ret;
  }


#ifdef PYTHON_PROPERTIES
  %pythoncode %{
    @property
    def state(self):
      return self._get_flag()

    @state.setter
    def state(self, theflag):
      self._set_flag(theflag)
  %}
#endif
} // extend Flag_bool
%extend Flag {
#ifdef PYTHON_PROPERTIES
  int _get_flag()
#else
  int get_flag()
#endif
  {
    int theFlag = self->flag();
    return theFlag;
  }

#ifdef PYTHON_PROPERTIES
  void _set_flag(int theFlag)
#else
  void set_flag(int theFlag)
#endif
  {
    self->flag() = theFlag;
  }
  clipper::datatypes::Flag copy()
  {
    clipper::datatypes::Flag ret;
    ret = *self;
    return ret;
  }
#ifdef PYTHON_PROPERTIES
  %pythoncode %{
    @property
    def flag(self):
      return self._get_flag()

    @flag.setter
    def flag(self, theFlag):
      self._set_flag(theFlag)
  %}
#endif
  } // extend Flag
} // namespace datatypes
} // namespace clipper


//%rename (to_complex_float) operator complex<float>();
//%rename (to_complex_double) operator complex<double>();



/*
 The singular data types we can expand as templates and instantiate later,
 saving a few dozen lines of duplicated code. Unfortunately SWIG doesn't
 seem to be quite smart enough to do this trick for classes of the form
 template < template < T > > (or I'm not smart enough to work out how), so
 we have to instantiate the float and double versions and then extend them.
 To avoid doubling up on code, we can use a little SWIG macro magic.

 -- Tristan
*/
namespace clipper
{

%define COPY_DATATYPE_HELPER(DATATYPE)
%extend datatypes::DATATYPE {
  clipper::datatypes::DATATYPE<dtype> copy()
  {
    clipper::datatypes::DATATYPE<dtype> ret;
    ret = *self;
    return ret;
  }
}
%enddef
COPY_DATATYPE_HELPER(F_sigF)
COPY_DATATYPE_HELPER(F_sigF_ano)
COPY_DATATYPE_HELPER(I_sigI)
COPY_DATATYPE_HELPER(E_sigE)
COPY_DATATYPE_HELPER(F_phi)
COPY_DATATYPE_HELPER(ABCD)

  %extend datatypes::F_phi{

    std::complex<dtype> as_complex() {
      return std::complex<dtype>(*self);
    }
    clipper::datatypes::F_phi<dtype>  __add__(const clipper::datatypes::F_phi<dtype> &h2)
    {
      return *self+h2;
    }
    clipper::datatypes::F_phi<dtype>  __sub__(const clipper::datatypes::F_phi<dtype> &h2)
    {
      return *self-h2;
    }
    clipper::datatypes::F_phi<dtype>  __neg__()
    {
      return -*self;
    }
  } // extend datatypes::F_phi<float>

  %extend datatypes::ABCD {
    clipper::datatypes::ABCD<dtype>  __add__(const clipper::datatypes::ABCD<dtype> &h2)
    {
      return *self+h2;
    }
    void vals(double numpy_double_out[4]) {
      numpy_double_out[0] = self->a();
      numpy_double_out[1] = self->b();
      numpy_double_out[2] = self->c();
      numpy_double_out[3] = self->d();
    }
  } // extend datatypes::ABCD


  %template(F_sigF_float) clipper::datatypes::F_sigF<float>;
  %template(F_sigF_double) clipper::datatypes::F_sigF<double>;

  %template(F_sigF_ano_float) clipper::datatypes::F_sigF_ano<float>;
  %template(F_sigF_ano_double) clipper::datatypes::F_sigF_ano<double>;

  %template(I_sigI_float) clipper::datatypes::I_sigI<float>;
  %template(I_sigI_double) clipper::datatypes::I_sigI<double>;

  %template(E_sigE_float) clipper::datatypes::E_sigE<float>;
  %template(E_sigE_double) clipper::datatypes::E_sigE<double>;

  %template(ABCD_float) clipper::datatypes::ABCD<float>;
  %template(ABCD_double) clipper::datatypes::ABCD<double>;

  %template(Phi_fom_float) clipper::datatypes::Phi_fom<float>;
  %template(Phi_fom_double) clipper::datatypes::Phi_fom<double>;

  %template(F_phi_float) clipper::datatypes::F_phi<float>;
  %template(F_phi_double) clipper::datatypes::F_phi<double>;

  %template(HKL_data_Flag) HKL_data< clipper::datatypes::Flag>;
  %template(HKL_data_Flag_bool) HKL_data< clipper::datatypes::Flag_bool>;

  /**********************
   *   HKL_data_Flag_bool
   **********************
  */

%define CATCH_NULL_ARRAY()
if (self->is_null()) {
  throw std::length_error("Array is not initialised!");
}
%enddef


  %extend HKL_data<clipper::datatypes::Flag_bool> {
    HKL_data<clipper::datatypes::Flag_bool> __invert__()
    {
      CATCH_NULL_ARRAY()
      return !(*self);
    }
    HKL_data<clipper::datatypes::Flag_bool> __or__(const HKL_data<clipper::datatypes::Flag_bool> &d1)
    {
      CATCH_NULL_ARRAY()
      return (*self) | d1;
    }
    HKL_data<clipper::datatypes::Flag_bool> __xor__(const HKL_data<clipper::datatypes::Flag_bool> &d1)
    {
      CATCH_NULL_ARRAY()
      return (*self) ^ d1;
    }
    HKL_data<clipper::datatypes::Flag_bool> __and__(const HKL_data<clipper::datatypes::Flag_bool> &d1)
    {
      CATCH_NULL_ARRAY()
      return (*self) & d1;
    }
    HKL_data<clipper::datatypes::Flag_bool>  copy()
    {
      HKL_data<clipper::datatypes::Flag_bool> ret;
      ret = *self;
      return ret;
    }

    clipper::datatypes::Flag_bool& __getitem__(int i)
    {
      CATCH_NULL_ARRAY()
      int sz=(self->base_hkl_info()).num_reflections();
      i = (i < 0) ? sz + i : i;
      if (i >= sz || i < 0) {
        throw std::out_of_range("");
      }
      return (*self)[i];
    }
    size_t __len__()
    {
      CATCH_NULL_ARRAY()
      return (self->base_hkl_info()).num_reflections();
    }
  } // extend HKL_data<clipper::datatypes::Flag_bool>

  /**********************
   *   HKL_data_Flag
   **********************
  */

  %extend HKL_data<clipper::datatypes::Flag> {
    HKL_data<clipper::datatypes::Flag_bool> __eq__(const int& n)
    {
      CATCH_NULL_ARRAY()
      return (*self) == n;
    }
    HKL_data<clipper::datatypes::Flag_bool> __ne__(const int& n)
    {
      CATCH_NULL_ARRAY()
      return (*self) != n;
    }
    HKL_data<clipper::datatypes::Flag_bool> __ge__(const int& n)
    {
      CATCH_NULL_ARRAY()
      return (*self) >= n;
    }
    HKL_data<clipper::datatypes::Flag_bool> __le__(const int& n)
    {
      CATCH_NULL_ARRAY()
      return (*self) <= n;
    }
    HKL_data<clipper::datatypes::Flag_bool> __gt__(const int& n)
    {
      CATCH_NULL_ARRAY()
      return (*self) > n;
    }
    HKL_data<clipper::datatypes::Flag_bool> __lt__(const int& n)
    {
      CATCH_NULL_ARRAY()
      return (*self) < n;
    }
    clipper::datatypes::Flag& __getitem__(int i)
    {
      CATCH_NULL_ARRAY()
      int sz=(self->base_hkl_info()).num_reflections();
      i = (i < 0) ? sz + i : i;
      if (i >= sz || i < 0) {
        throw std::out_of_range("");
      }
      return (*self)[i];
    }
    size_t __len__()
    {
      CATCH_NULL_ARRAY()
      return (self->base_hkl_info()).num_reflections();
    }
    HKL_data<clipper::datatypes::Flag>  copy()
    {
      HKL_data<clipper::datatypes::Flag> ret;
      ret = *self;
      return ret;
    }
  } // extend HKL_data<clipper::datatypes::Flag>



%define HKL_DATA_F_PHI_HELPER(TYPE,DATAXX)


  %extend HKL_data< clipper::DATAXX::F_phi > {
    HKL_data<clipper::datatypes::F_phi<TYPE> >  copy()
    {
      HKL_data<clipper::datatypes::F_phi<TYPE> > ret;
      ret = *self;
      return ret;
    }
    /*
       This would be nice, but what do I do with memo?
       Python way is:
       memo[id(self)] = result (where result is new class)
       How on earth can I do this in Python?
       But without this method os.deepcopy will never work.
    HKL_data<clipper::datatypes::F_phi<float> >  __deepcopy__(PyObject *memo){
      HKL_data<clipper::data32::F_phi> ret;
      ret = *self;
      return ret;
    }
    */
    HKL_data<clipper::datatypes::F_phi<TYPE> > __add__(const HKL_data<clipper::datatypes::F_phi<TYPE> > &h2)
    {
      CATCH_NULL_ARRAY()
      return *self+h2;
    }
    HKL_data<clipper::datatypes::F_phi<TYPE> > __sub__(const HKL_data<clipper::datatypes::F_phi<TYPE> > &h2)
    {
      CATCH_NULL_ARRAY()
      return *self-h2;
    }
    HKL_data<clipper::datatypes::F_phi<TYPE> > __neg__()
    {
      CATCH_NULL_ARRAY()
      return -*self;
    }
    HKL_data<clipper::datatypes::F_phi<TYPE> > __mul__(const TYPE &s)
    {
      CATCH_NULL_ARRAY()
      return *self*s;
    }
    HKL_data<clipper::datatypes::F_phi<TYPE> > __rmul__(const TYPE &s)
    {
      CATCH_NULL_ARRAY()
      return *self*s;
    }


    void compute_neg(const HKL_data< clipper::datatypes::F_phi<TYPE> > &fphi )
    {
      CATCH_NULL_ARRAY()
      self->compute( fphi, clipper::DATAXX::Compute_neg_fphi() );
    }
    void compute_add_fphi(const HKL_data< clipper::datatypes::F_phi<TYPE> > &fphi1,
    const HKL_data< clipper::datatypes::F_phi<TYPE> > &fphi2)
    {
      CATCH_NULL_ARRAY()
      self->compute( fphi1, fphi2, clipper::DATAXX::Compute_add_fphi() );
    }
    void compute_sub_fphi(const HKL_data< clipper::datatypes::F_phi<TYPE> > &fphi1,
    const HKL_data< clipper::datatypes::F_phi<TYPE> > &fphi2)
    {
      CATCH_NULL_ARRAY()
      self->compute( fphi1, fphi2, clipper::DATAXX::Compute_sub_fphi() );
    }
    void compute_from_fsigf_phifom(const HKL_data< clipper::datatypes::F_sigF<TYPE> > &fsigf,
    const HKL_data< clipper::datatypes::Phi_fom<TYPE> > &phifom )
    {
      CATCH_NULL_ARRAY()
      self->compute( fsigf, phifom, clipper::DATAXX::Compute_fphi_from_fsigf_phifom() );
    }
    void compute_scale_u_iso_fphi(const TYPE &scale, const TYPE &u_value,
    const HKL_data< clipper::datatypes::F_phi<TYPE> > &fphi )
    {
      CATCH_NULL_ARRAY()
      self->compute( fphi, clipper::DATAXX::Compute_scale_u_iso_fphi(scale, u_value) );
    }
    void compute_scale_u_aniso_fphi(const TYPE &scale, const clipper::U_aniso_orth &u_value,
    const HKL_data< clipper::datatypes::F_phi<TYPE> > &fphi )
    {
      CATCH_NULL_ARRAY()
      self->compute( fphi, clipper::DATAXX::Compute_scale_u_aniso_fphi(scale, u_value) );
    }


  } // extend HKL_data<clipper::data32::F_phi >

%enddef

%template(HKL_data_F_phi_float) HKL_data< clipper::data32::F_phi >;
HKL_DATA_F_PHI_HELPER(float,data32)
%template(HKL_data_F_phi_double) HKL_data< clipper::data64::F_phi >;
HKL_DATA_F_PHI_HELPER(double,data64)


%define HKL_DATA_ABCD_HELPER(TYPE,DATAXX)

%extend HKL_data<clipper::DATAXX::ABCD> {
  HKL_data<clipper::datatypes::ABCD<TYPE> > __add__(const HKL_data<clipper::datatypes::ABCD<TYPE> > &h2)
  {
    CATCH_NULL_ARRAY()
    return *self+h2;
  }
  HKL_data<clipper::datatypes::ABCD<TYPE> > copy()
  {
    HKL_data<clipper::DATAXX::ABCD> ret;
    ret = *self;
    return ret;
  }

  void compute_from_phi_fom(const HKL_data< clipper::datatypes::Phi_fom<TYPE> > &phiw)
  {
    CATCH_NULL_ARRAY()
    self->compute( phiw, clipper::DATAXX::Compute_abcd_from_phifom() );
  }
  void compute_add_abcd(const HKL_data< clipper::datatypes::ABCD<TYPE> > &abcd1,
  const HKL_data< clipper::datatypes::ABCD<TYPE> > &abcd2)
  {
    CATCH_NULL_ARRAY()
    self->compute( abcd1, abcd2, clipper::DATAXX::Compute_add_abcd() );
  }
} // extend HKL_data<clipper::data32::ABCD>

%enddef

%template(HKL_data_ABCD_float) HKL_data< clipper::data32::ABCD >;
HKL_DATA_ABCD_HELPER(float,data32)
%template(HKL_data_ABCD_double) HKL_data< clipper::data64::ABCD >;
HKL_DATA_ABCD_HELPER(double,data64)


%define HKL_DATA_E_SIGE_HELPER(TYPE,DATAXX)


%extend HKL_data<clipper::DATAXX::E_sigE> {
  void scaleBySqrtResolution(const clipper::ResolutionFn &escale)
  {
    CATCH_NULL_ARRAY()
    for ( clipper::HKL_data_base::HKL_reference_index ih = self->first(); !ih.last(); ih.next() )
      if ( !(*self)[ih].missing() ) (*self)[ih].scale( sqrt( escale.f(ih) ) );
  }
  void scaleByResolution(const clipper::ResolutionFn &escale)
  {
    CATCH_NULL_ARRAY()
    for ( clipper::HKL_data_base::HKL_reference_index ih = self->first(); !ih.last(); ih.next() )
      if ( !(*self)[ih].missing() ) (*self)[ih].scale( escale.f(ih) );
  }
  HKL_data<clipper::datatypes::E_sigE<TYPE> >  copy()
  {
    CATCH_NULL_ARRAY()
    HKL_data<clipper::DATAXX::E_sigE> ret;
    ret = *self;
    return ret;
  }
  void compute_from_fsigf(const HKL_data< clipper::datatypes::F_sigF<TYPE> > &fsigf )
  {
    CATCH_NULL_ARRAY()
    self->compute( fsigf, clipper::DATAXX::Compute_EsigE_from_FsigF() );
  }
} // extend HKL_data<clipper::data32::E_sigE>

%enddef

%template(HKL_data_E_sigE_float) HKL_data< clipper::data32::E_sigE >;
HKL_DATA_E_SIGE_HELPER(float, data32)
%template(HKL_data_E_sigE_double) HKL_data< clipper::data64::E_sigE >;
HKL_DATA_E_SIGE_HELPER(double,data64)


%define HKL_DATA_PHI_FOM_HELPER(TYPE,DATAXX)

%extend HKL_data<clipper::DATAXX::Phi_fom> {
  void compute_from_abcd(const HKL_data< clipper::datatypes::ABCD<TYPE> > &abcd)
  {
    CATCH_NULL_ARRAY()
    self->compute( abcd, clipper::DATAXX::Compute_phifom_from_abcd() );
  }
  HKL_data<clipper::datatypes::Phi_fom<TYPE> >  copy()
  {
    HKL_data<clipper::DATAXX::Phi_fom> ret;
    ret = *self;
    return ret;
  }
} // extend HKL_data<clipper::data32::Phi_fom>

%enddef

%template(HKL_data_Phi_fom_float) HKL_data< clipper::data32::Phi_fom >;
HKL_DATA_PHI_FOM_HELPER(float,data32)
%template(HKL_data_Phi_fom_double) HKL_data< clipper::data64::Phi_fom >;
HKL_DATA_PHI_FOM_HELPER(double,data64)


%define HKL_DATA_F_SIGF_HELPER(TYPE,DATAXX)

%extend HKL_data<clipper::datatypes::F_sigF<TYPE> > {
  void compute_mean_from_fano(const HKL_data< clipper::datatypes::F_sigF_ano<TYPE> > &fano)
  {
    CATCH_NULL_ARRAY()
    self->compute( fano, clipper::DATAXX::Compute_mean_fsigf_from_fsigfano() );
  }
  void compute_diff_from_fano(const HKL_data< clipper::datatypes::F_sigF_ano<TYPE> > &fano)
  {
    CATCH_NULL_ARRAY()
    self->compute( fano, clipper::DATAXX::Compute_diff_fsigf_from_fsigfano() );
  }
  void compute_scale_u_iso_fsigf(const TYPE &scale, const TYPE &u_value,
  const HKL_data< clipper::datatypes::F_sigF<TYPE> > &fsigf )
  {
    CATCH_NULL_ARRAY()
    self->compute( fsigf, clipper::DATAXX::Compute_scale_u_iso_fsigf(scale, u_value) );
  }
  void compute_scale_u_aniso_fsigf(const TYPE &scale, const clipper::U_aniso_orth &u_value,
  const HKL_data< clipper::datatypes::F_sigF<TYPE> > &fsigf )
  {
    CATCH_NULL_ARRAY()
    self->compute( fsigf, clipper::DATAXX::Compute_scale_u_aniso_fsigf(scale, u_value) );
  }
  HKL_data<clipper::datatypes::F_sigF<TYPE> >  copy()
  {
    CATCH_NULL_ARRAY()
    HKL_data<clipper::DATAXX::F_sigF> ret;
    ret = *self;
    return ret;
  }

} // extend HKL_data<clipper::data32::F_sigF>
%enddef

%template(HKL_data_F_sigF_float) HKL_data< clipper::data32::F_sigF >;
HKL_DATA_F_SIGF_HELPER(float,data32)
%template(HKL_data_F_sigF_double) HKL_data< clipper::data64::F_sigF >;
HKL_DATA_F_SIGF_HELPER(double,data64)


%define HKL_DATA_F_SIGF_ANO_HELPER(TYPE,DATAXX)

%extend HKL_data<clipper::DATAXX::F_sigF_ano> {
  void compute_scale_u_iso_fsigfano(const TYPE &scale, const TYPE &u_value,
  const HKL_data< clipper::datatypes::F_sigF_ano<TYPE> > &fsigfano )
  {
    CATCH_NULL_ARRAY()
    self->compute( fsigfano, clipper::DATAXX::Compute_scale_u_iso_fsigfano(scale, u_value) );
  }
  void compute_scale_u_aniso_fsigfano(const TYPE &scale, const clipper::U_aniso_orth &u_value,
  const HKL_data< clipper::datatypes::F_sigF_ano<TYPE> > &fsigfano )
  {
    CATCH_NULL_ARRAY()
    self->compute( fsigfano, clipper::DATAXX::Compute_scale_u_aniso_fsigfano(scale, u_value) );
  }
  HKL_data<clipper::datatypes::F_sigF_ano<TYPE> >  copy()
  {
    CATCH_NULL_ARRAY()
    HKL_data<clipper::DATAXX::F_sigF_ano> ret;
    ret = *self;
    return ret;
  }
} // extend HKL_data<clipper::data32::F_sigF_ano>

%enddef

%template(HKL_data_F_sigF_ano_float) HKL_data< clipper::data32::F_sigF_ano >;
HKL_DATA_F_SIGF_ANO_HELPER(float, data32)
%template(HKL_data_F_sigF_ano_double) HKL_data< clipper::data64::F_sigF_ano >;
HKL_DATA_F_SIGF_ANO_HELPER(double, data64)


%define HKL_DATA_I_SIGI_HELPER(TYPE,DATAXX)


%extend HKL_data<clipper::DATAXX::I_sigI> {
  void compute_scale_u_iso_isigi(const TYPE &scale, const TYPE &u_value,
  const HKL_data< clipper::datatypes::I_sigI<TYPE> > &isigi )
  {
    CATCH_NULL_ARRAY()
    self->compute( isigi, clipper::DATAXX::Compute_scale_u_iso_isigi(scale, u_value) );
  }
  void compute_scale_u_aniso_isigi(const TYPE &scale, const clipper::U_aniso_orth &u_value,
  const HKL_data< clipper::datatypes::I_sigI<TYPE> > &isigi )
  {
    CATCH_NULL_ARRAY()
    self->compute( isigi, clipper::DATAXX::Compute_scale_u_aniso_isigi(scale, u_value) );
  }
  HKL_data<clipper::datatypes::I_sigI<TYPE> >  copy()
  {
    CATCH_NULL_ARRAY()
    HKL_data<clipper::DATAXX::I_sigI> ret;
    ret = *self;
    return ret;
  }
} // extend HKL_data<clipper::data32::I_sigI>
%enddef

%template(HKL_data_I_sigI_float) HKL_data< clipper::data32::I_sigI >;
HKL_DATA_I_SIGI_HELPER(float,data32)
%template(HKL_data_I_sigI_double) HKL_data< clipper::data64::I_sigI >;
HKL_DATA_I_SIGI_HELPER(double,data64)



%define HKL_COMMON_INNER_HELPER(TYPE,DATAXX,DTYPE)

%extend HKL_data<clipper::DATAXX::DTYPE>
{
  void _getDataNumpy(TYPE *numpy_array, int n1, int n2)
  {
    CATCH_NULL_ARRAY()
    int i=0;
    for(clipper::HKL_data_base::HKL_reference_index ih = self->first(); !ih.last(); ih.next() ) {
      if(!((*self)[ih].missing())) {
        std::vector<xtype> thisData(self->data_size());
        self->data_export(ih.hkl(),&(thisData[0]));
        for(unsigned idat=0; idat<self->data_size(); ++idat, i++) {
          numpy_array[i] = thisData[idat];
        }
      } else {
        for(unsigned idat=0; idat<self->data_size(); ++idat, i++) {
          numpy_array[i] = std::numeric_limits<TYPE>::quiet_NaN();
        }
      }
    }
  }

  %pythoncode %{
    def as_numpy(self, target = None):
      if target is None:
        import numpy
        dtype = 'TYPE'
        if dtype == 'float':
          arr_type = numpy.float32
        else:
          arr_type = numpy.double
        target = numpy.empty((len(self), self.data_size()), arr_type)
      self._getDataNumpy(target)
      return target
  %}



  std::vector<std::vector<TYPE> > getData()
  {
    CATCH_NULL_ARRAY()
    std::vector<std::vector<TYPE> > allData;
    for(clipper::HKL_data_base::HKL_reference_index ih = self->first(); !ih.last(); ih.next() ) {
      std::vector<TYPE> thisDataf(self->data_size(), std::numeric_limits<TYPE>::quiet_NaN());
      if(!((*self)[ih].missing())) {
        std::vector<xtype> thisData(self->data_size());
        self->data_export(ih.hkl(),&(thisData[0]));
        std::vector<TYPE> thisDataf(self->data_size());
        for(unsigned idat=0; idat<self->data_size(); ++idat) {
          thisDataf[idat] = thisData[idat];
        }
      }
      allData.push_back(thisDataf);

    }
    return allData;
  }
  clipper::DATAXX::DTYPE& __getitem__(int i)
  {
    CATCH_NULL_ARRAY()
    int sz=(self->base_hkl_info()).num_reflections();
    i = (i < 0) ? sz + i : i;
    if (i >= sz || i < 0) {
      throw std::out_of_range("");
    }
    return (*self)[i];
  }
  size_t __len__()
  {
    CATCH_NULL_ARRAY()
    return (self->base_hkl_info()).num_reflections();
  }


}

%enddef

%define HKL_COMMON_OUTER_HELPER(DATATYPE)
HKL_COMMON_INNER_HELPER(float,data32,DATATYPE)
HKL_COMMON_INNER_HELPER(double,data64,DATATYPE)
%enddef

HKL_COMMON_OUTER_HELPER(F_phi)
HKL_COMMON_OUTER_HELPER(I_sigI)
HKL_COMMON_OUTER_HELPER(F_sigF)
HKL_COMMON_OUTER_HELPER(E_sigE)
HKL_COMMON_OUTER_HELPER(F_sigF_ano)
HKL_COMMON_OUTER_HELPER(ABCD)
HKL_COMMON_OUTER_HELPER(Phi_fom)



} // namespace clipper
